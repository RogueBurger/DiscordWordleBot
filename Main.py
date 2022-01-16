import asyncio
import hashlib
import os
import urllib.request
import functools
import signal
import sys
import logging

from discord import Message
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError

from Config import Config, ConfigValidationError
from Ping.Ping import Ping
from Wordle.Lock import Lock, LockNotOwnedError, LockNotFoundError
from Wordle.Wordle import Wordle
from Wordle.Words import Words
from Wordle.RedisClient import RedisClient, RedisConnectionError
from Wordle.Store import InMemoryLock, InMemoryStore, RedisStore, Store


def shutdown(sig: signal, event: asyncio.Event, logger: logging.Logger):
    logger.info(f'Received signal {sig.name}, exiting')
    event.set()


async def run(config: Config, logger: logging.Logger):
    bot = commands.Bot(command_prefix='%')
    loop = bot.loop

    stopped = asyncio.Event()
    for sig in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(
            sig, functools.partial(shutdown, sig, stopped, logger))

    state_backend: Store = InMemoryStore()
    lock: Lock = InMemoryLock()

    if config.redis.enable:
        try:
            redis = RedisClient(host=config.redis.host, port=config.redis.port)
            await redis.ping()
        except RedisConnectionError as e:
            logger.error(f'Unable to connect to Redis backend: {e}')
            return

        state_backend = RedisStore(redis)
        lock_key = hashlib.sha256(config.token.encode()).hexdigest()
        lock = redis.lock(
            f'wordlebot:lock:{lock_key}', timeout=10, blocking_timeout=1)

    bot.add_cog(Wordle(bot, state_backend=state_backend, logger=logger))
    bot.add_cog(Ping(bot))

    @bot.event
    async def on_ready():
        logger.info(f'Bot started with {state_backend.type_desc} state')

    @bot.event
    async def on_error(event_method: str, *args, **kwargs):
        if len(args) > 1 and isinstance(args[1], CommandInvokeError):
            if hasattr(args[1], 'original') and isinstance(args[1].original, RedisConnectionError):
                return logger.error(args[1])
        raise

    @bot.event
    async def on_message(msg: Message):
        if config.deny_channels in config.deny_channels:
            return

        if config.allow_channels and msg.channel.id not in config.allow_channels:
            return

        await bot.process_commands(msg)

    async def acquire_lock(locked: asyncio.Event, stopped: asyncio.Event):
        while True:
            if stopped.is_set():
                return

            await asyncio.sleep(1)
            try:
                if await lock.acquire():
                    locked.set()
                    return
            except RedisConnectionError as e:
                logger.warning(f'RedisConnectionError: {e}')
                await asyncio.sleep(5)

    async def extend_lock(
            unlocked_event: asyncio.Event,
            stop_event: asyncio.Event,
            new_ttl: float = 10.0):

        while True:
            if stop_event.is_set():
                unlocked_event.set()
                return

            try:
                await asyncio.sleep(5)
                await asyncio.wait_for(
                    lock.extend(additional_time=new_ttl, replace_ttl=True),
                    timeout=1.0)
            except asyncio.TimeoutError:
                continue
            except RedisConnectionError as e:
                # TODO: Exponential backoff
                logger.warning(f'RedisConnectionError: {e}')
            except Exception as e:
                logger.warning(
                    f'Failed to extend lock. {e.__class__.__name__}: {e}')
                unlocked_event.set()
                return

    locked = asyncio.Event()
    unlocked = asyncio.Event()

    logger.info('Attempting to acquire lock...')

    while not stopped.is_set():
        await acquire_lock(locked, stopped)
        unlocked.clear()

        if locked.is_set() and not stopped.is_set():
            logger.info('Lock acquired')

            tasks = [
                loop.create_task(extend_lock(
                    unlocked, stopped), name='extend_lock'),
                loop.create_task(bot.start(config.token), name='bot')]

            await unlocked.wait()

            for task in tasks:
                logging.info(f'Cancelling task: {task.get_name()}')
                task.cancel()

    await stopped.wait()
    try:
        await lock.release()
    except LockNotOwnedError:
        ...


def main():
    # TODO: Extract all this setup to a separate function or class

    logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s %(levelname)-.4s [%(name)-16s] %(message)s',
        level=logging.ERROR)

    try:
        config = Config()
    except ConfigValidationError as e:
        logging.error(e)
        exit(1)

    logging.getLogger('WordleBot').setLevel(config.log_level)
    logger = logging.getLogger('WordleBot')

    if not os.path.exists(Words.DATABASE):
        logger.info('Performing first time setup.')
        logger.info('Creating database...')
        Words.create_db()
        logger.info('Downloading wordlist...')
        urllib.request.urlretrieve(config.wordlist, Words.WORDLIST)
        logger.info('Seeding database...')
        Words.seed()
        logger.info('Setup complete.')

    asyncio.run(run(config, logger))


if __name__ == '__main__':
    main()
