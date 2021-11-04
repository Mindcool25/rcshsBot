#IMPORTS
from typing import Container
import nextcord
from nextcord.ext import commands
import botPrefixes as bp
import os
from os import listdir
from Libs.pretty_help import PrettyHelp, DefaultMenu

# Welcome and Rules channel link
WELCOME_MESSAGE_ID  = 846940613478973453
RULES_CHANNEL       = 848980735754240040

#NOT TO BE EDITED!
with open("token.txt") as f:
    TOKEN = f.readline()

def get_prefix(bot, message):
    return commands.when_mentioned_or(*bp.prefixes)(bot, message)

intents = nextcord.Intents.all()
intents.members = True

bot = commands.Bot(
    command_prefix=get_prefix,
    description="Bot for the r/CSHighschoolers discord server",
    intents=intents
)

# Help Command
menu = DefaultMenu(page_left="\u2B05", page_right="\u27A1", remove="\u274C", active_time=5)
version = "1.0.5"
user_name = "r/cshighschooler"
ending_note = f"{user_name}-{version}"

bot.help_command = PrettyHelp(menu=menu, ending_note=ending_note)

if __name__ == "__main__":
    for fn in listdir("cogs"):
        if fn.endswith(".py"):
            bot.load_extension(f"cogs.{fn[:-3]}")
            print(f"Loading cogs.{fn[:-3]}")
    
    for fn in listdir("cogs/utils"):
        if fn.endswith(".py"):
            bot.load_extension(f"cogs.utils.{fn[:-3]}")
            print(f"Loading cogs.utils.{fn[:-3]}")
    
    for fn in listdir("cogs/user"):
        if fn.endswith(".py"):
            bot.load_extension(f"cogs.user.{fn[:-3]}")
            print(f"Loading cogs.user.{fn[:-3]}")

print("Loaded extensions")

@bot.event
async def on_ready():
    print('------')
    print('Logged In As:')
    print(f"Username: {bot.user.name}\nID: {bot.user.id}")
    print('------')

@bot.event
async def on_member_join(member):
    try:
        channel = bot.get_channel(WELCOME_MESSAGE_ID)
        rules   = bot.get_channel(RULES_CHANNEL)
        try:
            value=f"Welcome {member.mention} to {member.guild.name}' Discord server! Check out our rules over at {rules.mention} and have a nice stay!"
            await channel.send(value)
        except Exception as e:
            raise e
    except Exception as e:
        raise e

"""
This will handle events but if you dont handle every single error you can get, some might slip by without you knowing.
For more info watch (https://youtu.be/_2ifplRzQtM?list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ)
"""
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.reply("Please pass in all required arguments.")

bot.run(TOKEN, reconnect=True)
