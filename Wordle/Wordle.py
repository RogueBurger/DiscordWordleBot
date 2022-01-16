import logging
from typing import Optional

from discord.ext import commands
from discord.ext.commands import Context, Bot, CommandError, CommandNotFound

from .Canvas import Canvas
from .Game import Game
from .GameManager import GameManager
from .Lock import LockNotFoundError
from .Store import GameNotFoundError, Store
from .Words import Words


class Wordle(commands.Cog):
    def __init__(self, bot: Bot, state_backend: Store, logger: logging.Logger):
        self.bot = bot
        self.canvas = Canvas()
        self.games: GameManager = GameManager(state_backend)
        self.logger: logging.Logger = logger.getChild(self.__class__.__name__)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        original = error if not hasattr(error, 'original') else error.original

        if isinstance(original, CommandNotFound):
            self.logger.debug(error)
            return

        if isinstance(original, GameNotFoundError) or isinstance(original, LockNotFoundError):
            return await ctx.send(
                'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
            )

        raise error

    @commands.command(aliases=['s'])
    async def start(self, ctx: Context, word_length: Optional[int] = 5, mode: Optional[str] = Game.EASY):
        try:
            if await self.games.get_current_game(ctx.message.channel.id):
                return await ctx.send(
                    'Game already in progress. Use `%guess <word>` to continue playing, or `%stop` to end the game early.'
                )
        except GameNotFoundError:
            pass

        if word_length < 2 or word_length > 20:
            return await ctx.send('Unfortunately I only support words with between 2 and 20 letters.')

        game = Game(word_length=word_length, mode=mode)

        self.logger.debug(f'New game started: {game.target.word}')

        if not game.target:
            return await ctx.send('Unfortunately I can\'t find a word of that length.')

        await self.games.add_game(ctx.message.channel.id, game)

        await ctx.send(
            f'Game started. I\'m think of a word that is {word_length} letters long. Can you guess it?'
        )

        return

    @commands.command()
    async def stop(self, ctx: Context):
        game = await self.games.get_current_game(ctx.message.channel.id)

        word, definition = game.target.word, game.target.definition

        await self.games.stop_current_game(ctx.message.channel.id)
        await ctx.send(
            f'Game stopped. The answer was {word}: {definition}'
        )
        return

    @commands.command(aliases=['g'])
    async def guess(self, ctx: Context, word: Optional[str] = None):
        async with self.games.lock(ctx.message.channel.id):
            game = await self.games.get_current_game(ctx.message.channel.id)

            status, message, image = game.guess(word, self.canvas)
            await self.games.update_game(ctx.message.channel.id, game)

            if status in [Game.CORRECT, Game.FAILED]:
                await self.games.stop_current_game(ctx.message.channel.id)

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
        async with self.games.lock(ctx.message.channel.id):
            game = await self.games.get_current_game(ctx.message.channel.id)

            if not game.guesses:
                return await ctx.send(
                    'There have not been any guesses yet.'
                )

            return await ctx.send('Guesses so far:', file=game.progress.to_discord_file())

    @commands.command(aliases=['h'])
    async def hint(self, ctx: Context):
        async with self.games.lock(ctx.message.channel.id):
            game = await self.games.get_current_game(ctx.message.channel.id)

            return await ctx.send(
                'These letters haven\'t been tried yet:',
                file=game.get_unused_letters(self.canvas).to_discord_file()
            )
