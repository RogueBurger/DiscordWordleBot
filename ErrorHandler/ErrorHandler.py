import logging

from discord.ext import commands

from Wordle.RedisClient import RedisConnectionError


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger):
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.NotOwner):
            return await ctx.send('Only the bot owner can issue that command')

        if isinstance(error, commands.MemberNotFound):
            return await ctx.send('Member not found')

        log_msg = f'{error} (message="{ctx.message.content}")'

        if isinstance(error, commands.CommandInvokeError):
            if ctx.cog.has_error_handler() or hasattr(ctx.command, 'on_error'):
                return

            self.logger.warn(log_msg)
            return

        if isinstance(error, commands.CommandNotFound):
            self.logger.debug(log_msg)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            self.logger.debug(log_msg)
            return

        self.logger.error(log_msg)
        raise error

    async def on_command_invoke_error(self, ctx: commands.Context, error: commands.CommandInvokeError):
        if ctx.cog.has_error_handler() or hasattr(ctx.command, 'on_error'):
            return

        err = hasattr(error, 'original', error)

        if isinstance(err, RedisConnectionError):
            return

        raise error
