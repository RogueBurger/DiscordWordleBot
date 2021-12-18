from typing import Optional

from discord.ext import commands

from .Game import Game
from .Words import Words


class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games: dict = {}

    # TODO: Create a GameManager class instead of just a games dict to hold games and methods for accessing them
    def __get_current_game(self, channel_id: int):
        try:
            return self.games[channel_id]
        except KeyError:
            return None

    def __stop_current_game(self, channel_id):
        try:
            self.games.pop(channel_id)
            return True
        except KeyError:
            return False

    @commands.command(aliases=['s'])
    async def start(self, ctx, param: str = '5'):
        first_guess: Optional[str]
        word_length: int

        if self.__get_current_game(ctx.message.channel.id):
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

        self.games[ctx.message.channel.id] = Game(word_length)

        await ctx.send(
            f'Game started. I\'m think of a word that is {word_length} letter long. Can you guess it?'
        )

        if first_guess:
            await self.guess(ctx, first_guess)

        return

    @commands.command()
    async def stop(self, ctx):
        game = self.__get_current_game(ctx.message.channel.id)

        if game:
            await ctx.send(
                f'Game stopped. The answer was {game.target}: {game.definition}.'
            )
            self.__stop_current_game(ctx.message.channel.id)
            return

        return await ctx.send(
            'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
        )

    @commands.command(aliases=['g'])
    async def guess(self, ctx, word=None):
        game = self.__get_current_game(ctx.message.channel.id)

        if not game:
            return await ctx.send(
                'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
            )

        status, message = game.guess(word)
        if status == Game.CORRECT:
            self.__stop_current_game(ctx.message.channel.id)

        return await ctx.send(message)

    @commands.command(aliases=['d'])
    async def define(self, ctx, word):
        definitions = Words.get_definitions_by_word(word)

        if not definitions:
            return await ctx.send('I don\'t know what that word means, sorry!')

        await ctx.send(f'{word}:')
        for definition in definitions:
            text = definition[0].replace("\n", '')
            await ctx.send(f'* {text}')

        return

    @commands.command(aliases=['p'])
    async def progress(self, ctx):
        game = self.__get_current_game(ctx.message.channel.id)

        if not game:
            return await ctx.send(
                'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
            )

        guesses = game.get_history()
        return await ctx.send(
            'Guesses so far:\n' + '\n'.join([f'`{guess}`' for guess in guesses])
        )

    @commands.command()
    async def h(self, ctx):
        return await ctx.send('''
Commands:
`%start <word_length=5>` - starts a new game
`%stop` - ends the current game early
`%guess <word>` - makes a guess in the current game

Formatting:
After a guess, the bot will return your guess formatted according to these rules:
~~a~~ (strikethrough) - The letter does not appear in the word
`b` (backtick'd) - The letter appears in the word but in a different location
c (normal) - The letter appears in the word and is in the correct location

Special rules:
Once a game is started, each person is allowed to contribute a single guess.
        ''')
