import discord
from discord.ext import commands
import os


def get_prefix(bot, message):
    # The prefix for bot commands
    prefixes = ["."]

    return commands.when_mentioned_or(*prefixes)(bot, message)


extensions = ['cogs.basic']

bot = commands.Bot(
    command_prefix=get_prefix, description='Bot for the r/CSHighschoolers discord server')

if __name__ == '__main__':
    for extension in extensions:
        print(f"Loading {extension}...")
        bot.load_extension(extension)
print("Loaded extensions")


@bot.event
async def on_ready():
    print(
        f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n'
    )

bot.run('TOKEN', bot=True, reconnect=True)

