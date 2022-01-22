import aioredis.exceptions
from aioredis import Redis, ConnectionError

from Wordle.Lock import Lock, LockNotOwnedError, LockError


class RedisError(Exception):
    ...


class RedisConnectionError(RedisError):
    ...


class RedisClient(Redis):
    def path(self, *argv) -> str:
        return ':'.join(map(str, argv))

    async def execute_command(self, *args, **kwargs):
        try:
            return await super().execute_command(*args, **kwargs)
        except ConnectionError as e:
            raise RedisConnectionError(e)

    def lock(self, *args, **kwargs) -> Lock:
        try:
            return super().lock(*args, **kwargs)
        except aioredis.exceptions.LockNotOwnedError as e:
            raise LockNotOwnedError(e)
        except aioredis.exceptions.LockError as e:
            raise LockError(e)
