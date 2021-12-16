from typing import Optional

from discord.ext import commands

from .Game import Game


class Wordle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games: dict = {}

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

    @commands.command()
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

        if word_length < 2 or word_length > 15:
            return await ctx.send('Unfortunately I only support words with between 2 and 15 letters.')

        self.games[ctx.message.channel.id] = Game(word_length)

        await ctx.send(
            f'Game started. I\'m think of a word that is {word_length} letter long. Can you guess it?'
        )

        if first_guess:
            await self.guess(ctx, first_guess)

        return

    @commands.command()
    async def stop(self, ctx):
        if not self.__stop_current_game(ctx.message.channel.id):
            return await ctx.send(
                'There is no game currently in progress. To start a new one, use `%start <word_length=5>`.'
            )

        return await ctx.send(
            'Game stopped. To start a new one, use `%start <word_length=5>`.'
        )

    @commands.command()
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
