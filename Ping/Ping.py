import logging

from discord import Message, Member
from discord.ext import commands
from discord.ext.commands import Bot, Context
from Helpers.RandomText import RandomText


class Ping(commands.Cog):
    def __init__(self, bot: Bot, logger: logging.Logger):
        self.bot: Bot = bot
        self.banned_users: dict = {}
        self.logger = logger.getChild(self.__class__.__name__)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return

        if message.author.id in self.banned_users.keys():
            return

        if 'ping' in message.content:
            await message.channel.send(RandomText.all_star())

    # TODO: implement a real ban system instead of this silly in-memory one
    @commands.command()
    @commands.is_owner()
    async def unban(self, ctx: Context, member: Member):
        if member.id in self.banned_users.keys():
            self.banned_users.pop(member.id)
        await ctx.send('User unbanned')

    @commands.command()
    @commands.is_owner()
    async def ban(self, ctx: Context, member: Member):
        if member.id not in self.banned_users.keys():
            self.banned_users[member.id] = member
        await ctx.send('User banned')
