#IMPORTS
import discord
from discord.ext import commands

#NOT TO BE EDITED!
with open('token.txt') as f:
    TOKEN = f.readline()

def get_prefix(bot, message):
    # The prefix for bot commands
    prefixes = ["."]

    return commands.when_mentioned_or(*prefixes)(bot, message)

# If you make your own cog file, add it in a similar way that basic is added here, with 'cogs.<filename>'
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

bot.run(TOKEN, bot=True, reconnect=True)

