from typing import Optional

from discord.ext import commands
from discord.ext.commands import Context, Bot

from .Game import Game
from .GameManager import GameManager
from .Words import Words
from .Canvas import Canvas


class Wordle(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.canvas = Canvas()
        self.games: GameManager = GameManager()

    @commands.command(aliases=['s'])
    async def start(self, ctx: Context, param: str = '5'):
        first_guess: Optional[str]
        word_length: int

        if self.games.get_current_game(ctx.message.channel.id):
            return await ctx.send(
                'Game already in progress. Use `%guess <word>` to continue playing, or `%stop` to end the game early.'
            )

        if param.isnumeric():
            word_length = int(param)
            first_guess = None
        else:
            word_length = len(param)
            first_guess = param

        if word_length < 2 or word_length > 20:
            return await ctx.send('Unfortunately I only support words with between 2 and 20 letters.')

        self.games.add_game(ctx.message.channel.id, Game(self.canvas, word_length))

        await ctx.send(
            f'Game started. I\'m think of a word that is {word_length} letter long. Can you guess it?'
        )

        if first_guess:
            await self.guess(ctx, first_guess)

        return

    @commands.command()
    async def stop(self, ctx: Context):
        game = self.games.get_current_game(ctx.message.channel.id)

        if game:
            await ctx.send(
                f'Game stopped. The answer was {game.target.word}: {game.target.definition}'
            )
            self.games.stop_current_game(ctx.message.channel.id)
            return

        return await ctx.send(
            'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
        )

    @commands.command(aliases=['g'])
    async def guess(self, ctx: Context, word: Optional[str] = None):
        game = self.games.get_current_game(ctx.message.channel.id)

        if not game:
            return await ctx.send(
                'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
            )

        status, message, image = game.guess(word)
        if status == Game.CORRECT:
            self.games.stop_current_game(ctx.message.channel.id)

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
        game = self.games.get_current_game(ctx.message.channel.id)

        if not game:
            return await ctx.send(
                'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
            )

        if not game.guesses:
            return await ctx.send(
                'There have not been any guesses yet.'
            )

        return await ctx.send('Guesses so far:', file=game.progress.to_discord_file())
