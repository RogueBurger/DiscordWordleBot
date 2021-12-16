import random

import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_users = {}
        self.all_star = [
            'Somebody once told me the world is gonna roll me',
            'I ain\'t the sharpest tool in the shed',
            'She was looking kind of dumb with her finger and her thumb',
            'In the shape of an "L" on her forehead',
            'Well the years start coming and they don\'t stop coming',
            'Fed to the rules and I hit the ground running',
            'Didn\'t make sense not to live for fun',
            'Your brain gets smart but your head gets dumb',
            'So much to do, so much to see',
            'So what\'s wrong with taking the back streets?',
            'You\'ll never know if you don\'t go',
            'You\'ll never shine if you don\'t glow',
            'Hey now, you\'re an all-star, get your game on, go play',
            'Hey now, you\'re a rock star, get the show on, get paid',
            'And all that glitters is gold',
            'Only shooting stars break the mold',
            'It\'s a cool place and they say it gets colder',
            'You\'re bundled up now, wait \'til you get older',
            'But the meteor men beg to differ',
            'Judging by the hole in the satellite picture',
            'The ice we skate is getting pretty thin',
            'The water\'s getting warm so you might as well swim',
            'My world\'s on fire, how about yours?',
            'That\'s the way I like it and I\'ll never get bored',
            'Hey now, you\'re an all-star, get your game on, go play',
            'Hey now, you\'re a rock star, get the show on, get paid',
            'All that glitters is gold',
            'Only shooting stars break the mold',
            'Hey now, you\'re an all-star, get your game on, go play',
            'Hey now, you\'re a rock star, get the show, on get paid',
            'And all that glitters is gold',
            'Only shooting stars',
            'Somebody once asked could I spare some change for gas?',
            'I need to get myself away from this place',
            'I said, "Yup" what a concept',
            'I could use a little fuel myself',
            'And we could all use a little change',
            'Well, the years start coming and they don\'t stop coming',
            'Fed to the rules and I hit the ground running',
            'Didn\'t make sense not to live for fun',
            'Your brain gets smart but your head gets dumb',
            'So much to do, so much to see',
            'So what\'s wrong with taking the back streets?',
            'You\'ll never know if you don\'t go (go!)',
            'You\'ll never shine if you don\'t glow',
            'Hey now, you\'re an all-star, get your game on, go play',
            'Hey now, you\'re a rock star, get the show on, get paid',
            'And all that glitters is gold',
            'Only shooting stars break the mold',
            'And all that glitters is gold',
            'Only shooting stars break the mold'
        ]

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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in self.banned_users.keys():
            return

        if 'ping' in message.content:
            await message.channel.send(random.choice(self.all_star))
