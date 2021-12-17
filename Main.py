import os
import urllib.request

from discord.ext import commands
import yaml

from Ping.Ping import Ping
from Wordle.Wordle import Wordle
from Wordle.Words import Words

if __name__ == '__main__':
    try:
        with open("config.yaml", "r") as stream:
            config = yaml.safe_load(stream)
    except FileNotFoundError:
        print('Make sure you have a config.toml file with your bot\'s discord token.')
        exit()

    if not os.path.exists(Words.DATABASE):
        print('Performing first time setup.')
        print('Creating database...')
        Words.create_db()
        print('Downloading wordlist...')
        urllib.request.urlretrieve(config['wordlist'], Words.WORDLIST)
        print('Seeding database...')
        Words.seed()
        print('Setup complete.')

    bot = commands.Bot(command_prefix='%')
    bot.add_cog(Wordle(bot))
    bot.add_cog(Ping(bot))
    print('Bot started.')
    bot.run(config['token'])
