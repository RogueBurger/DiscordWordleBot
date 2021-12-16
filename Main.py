from discord.ext import commands
import yaml

from Ping.Ping import Ping
from Wordle.Wordle import Wordle

if __name__ == '__main__':
    try:
        with open("config.yaml", "r") as stream:
            config = yaml.safe_load(stream)
    except FileNotFoundError:
        print('Make sure you have a config.toml file with your bot\'s discord token.')
        exit()

    bot = commands.Bot(command_prefix='%')
    bot.add_cog(Wordle(bot))
    bot.add_cog(Ping(bot))
    bot.run(config['token'])
