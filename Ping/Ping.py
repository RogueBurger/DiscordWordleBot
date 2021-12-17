import random

import discord
from discord.ext import commands

from Helpers.RandomText import RandomText


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_users = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.id in self.banned_users.keys():
            return

        if 'ping' in message.content:
            await message.channel.send(RandomText.all_star())

    # TODO: implement a real ban system instead of this silly in-memory one
    @commands.command()
    async def unban(self, ctx, member: discord.Member):
        if ctx.author.id != 108633439984439296:
            return

        if member.id in self.banned_users.keys():
            self.banned_users.pop(member.id)
        await ctx.send('User unbanned')

    @commands.command()
    async def ban(self, ctx, member: discord.Member):
        if ctx.author.id != 108633439984439296:
            return

        if member.id not in self.banned_users.keys():
            self.banned_users[member.id] = member
        await ctx.send('User banned')
