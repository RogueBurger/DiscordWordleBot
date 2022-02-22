import logging
from typing import Optional

from discord.ext import commands
from discord.ext.commands import Context, Bot, CommandError

from Helpers.RandomText import RandomText

from Config import Config

from .Game import Game
from .GameManager import GameManager
from .Lock import LockNotFoundError
from .RedisClient import RedisConnectionError
from .Store import GameNotFoundError, Store
from .Words import Words


class Wordle(commands.Cog):
    def __init__(self, bot: Bot, config: Config, state_backend: Store, logger: logging.Logger):
        self.bot = bot
        self.games: GameManager = GameManager(
            canvas_config=config.canvas,
            backend=state_backend)
        self.logger: logging.Logger = logger.getChild(self.__class__.__name__)

    async def cog_command_error(self, ctx: Context, error: CommandError):
        err = getattr(error, 'original', error)

        if isinstance(err, GameNotFoundError) or isinstance(err, LockNotFoundError):
            return await ctx.send(
                'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
            )

        if isinstance(err, RedisConnectionError):
            self.logger.warn(
                f'Failed to process message "{ctx.message.content}" due to Redis connection error')
            return await ctx.send(f'_{RandomText.hal_9000()}_')

        raise err

    @commands.command(aliases=['s'])
    async def start(self, ctx: Context, word_length: Optional[int] = 5, mode: Optional[str] = Game.EASY):
        try:
            if await self.games.get_current_game(ctx.message.channel):
                return await ctx.send(
                    'Game already in progress. Use `%guess <word>` to continue playing, '
                    'or `%stop` to end the game early.'
                )
        except GameNotFoundError:
            pass

        if word_length < 2 or word_length > 20:
            return await ctx.send('Unfortunately I only support words with between 2 and 20 letters.')

        game = self.games.create_game(word_length=word_length, mode=mode)

        self.logger.debug(f'New game started: {game.target.word}')

        if not game.target:
            return await ctx.send('Unfortunately I can\'t find a word of that length.')

        await self.games.add_game(ctx.message.channel, game)

        if game.mode == Game.PUZZLE:
            await ctx.send(
                f'Alright, {RandomText.smarty()}...can you solve my puzzle?',
                file=game.progress.to_discord_file()
            )
        elif game.mode == Game.LIMITED:
            await ctx.send(
                f'Game started. I\'m think of a word that is {word_length} letters long. '
                f'You get {game.limit} guesses. Go!'
            )
        else:
            await ctx.send(
                f'Game started. I\'m think of a word that is {word_length} letters long. Can you guess it?'
            )

        return

    @commands.command()
    async def stop(self, ctx: Context):
        game = await self.games.get_current_game(ctx.message.channel)

        word, definition = game.target.word, game.target.definition

        await self.games.stop_current_game(ctx.message.channel)
        await ctx.send(
            f'Game stopped. The answer was {word}: {definition}'
        )
        return

    @commands.command(aliases=['g'])
    async def guess(self, ctx: Context, word: Optional[str] = None):
        async with self.games.lock(ctx.message.channel):
            game = await self.games.get_current_game(ctx.message.channel)

            status, message, image = game.guess(word, author_id=ctx.author.id)
            await self.games.update_game(ctx.message.channel, game)

            if status in [Game.CORRECT, Game.FAILED]:
                await self.games.stop_current_game(ctx.message.channel)

            if status == Game.FAILED:
                await ctx.send(file=image.to_discord_file())

            if status in [Game.INCORRECT, Game.CORRECT] and image:
                return await ctx.send(message, file=image.to_discord_file())

            return await ctx.send(message)

    @commands.command(aliases=['d'])
    async def define(self, ctx: Context, word: str):
        words = Words.get_by_word(word)

        if not words:
            return await ctx.send('I don\'t know what that word means, sorry!')

        await ctx.send(f'{word}:')
        for word in words:
            await ctx.send(f'* {word.definition}')

        return

    @commands.command(aliases=['p'])
    async def progress(self, ctx: Context):
        async with self.games.lock(ctx.message.channel):
            game = await self.games.get_current_game(ctx.message.channel)

            if not game.guesses:
                return await ctx.send(
                    'There have not been any guesses yet.'
                )

            return await ctx.send('Guesses so far:', file=game.progress.to_discord_file())

    @commands.command(aliases=['h'])
    async def hint(self, ctx: Context):
        async with self.games.lock(ctx.message.channel):
            game = await self.games.get_current_game(ctx.message.channel)

            return await ctx.send(
                file=game.draw_unused_letters().to_discord_file()
            )

    @commands.command(aliases=['hh'])
    async def known_letters(self, ctx: Context):
        async with self.games.lock(ctx.message.channel):
            game = await self.games.get_current_game(ctx.message.channel)
            return await ctx.send('Here\'s what you know:', file=game.draw_known_letters().to_discord_file())

    @commands.command()
    async def suggest(self, ctx: Context):
        game = await self.games.get_current_game(ctx.message.channel)

        if not game:
            return await ctx.send(
                'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
            )

        return await ctx.send(
            f'Try this one: {game.suggest()}'
        )
    @commands.command()
    async def cheat(self, ctx: Context):
        game = await self.games.get_current_game(ctx.message.channel)

        return await ctx.send(
            f'Fine...here you go...*cheater!*\n```{game.cheat()}```'
        )