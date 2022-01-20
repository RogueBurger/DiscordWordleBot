from typing import Optional

from discord import Embed
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
    async def start(self, ctx: Context, word_length: Optional[int] = 5, mode: Optional[str] = Game.EASY):
        if self.games.get_current_game(ctx.message.channel.id):
            return await ctx.send(
                'Game already in progress. Use `%guess <word>` to continue playing, or `%stop` to end the game early.'
            )

        if word_length < 2 or word_length > 20:
            return await ctx.send('Unfortunately I only support words with between 2 and 20 letters.')

        game = Game(self.canvas, word_length=word_length, mode=mode)

        if not game.target:
            return await ctx.send('Unfortunately I can\'t find a word of that length.')

        self.games.add_game(ctx.message.channel.id, game)

        if game.mode == Game.PUZZLE:
            await ctx.send(
                f'Puzzle started. I\'m think of a word that is {word_length} letters long. Can you guess it?',
                file=game.progress.to_discord_file()
            )
        else:
            await ctx.send(
                f'Game started. I\'m think of a word that is {word_length} letters long. Can you guess it?'
            )

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

        status, message, image = game.guess(word, ctx.author.id)
        if status in [Game.CORRECT, Game.FAILED]:
            self.games.stop_current_game(ctx.message.channel.id)

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

    @commands.command(aliases=['h'])
    async def hint(self, ctx: Context):
        game = self.games.get_current_game(ctx.message.channel.id)

        if not game:
            return await ctx.send(
                'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
            )

        return await ctx.send(
            'These letters haven\'t been tried yet:',
            file=game.get_unused_letters().to_discord_file()
        )

    @commands.command()
    async def suggest(self, ctx: Context):
        game = self.games.get_current_game(ctx.message.channel.id)

        if not game:
            return await ctx.send(
                'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
            )

        return await ctx.send(
            f'Try this one: {game.suggest()}'
        )
