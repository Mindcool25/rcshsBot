#IMPORTS
import nextcord
import botPrefixes as bp
import os
from nextcord.ext import commands

#NOT TO BE EDITED!
with open("token.txt") as f:
    TOKEN = f.readline()

def get_prefix(bot, message):
    return commands.when_mentioned_or(*bp.prefixes)(bot, message)

# If you make your own cog file, add it in a similar way that basic is added here, with 'cogs.<filename>'
extensions = ["cogs.basic","cogs.music", "cogs.moderation.prefix_control"]


bot = commands.Bot(
    command_prefix=get_prefix, description="Bot for the r/CSHighschoolers discord server")

if __name__ == "__main__":
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded {filename}")
        else:
            print(f"Unable to load {filename[:-3]}")


@bot.event
async def on_ready():
    print(
        f"\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {nextcord.__version__}\n"
    )

bot.run(TOKEN, reconnect=True) #  bot=True,
