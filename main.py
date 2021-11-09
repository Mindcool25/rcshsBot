#IMPORTS
from typing import Container
import nextcord
from nextcord.ext import commands
import botPrefixes as bp
import os
from os import listdir
from ruamel.yaml import YAML
from Libs.pretty_help import PrettyHelp, DefaultMenu
from Systems.levelsys import levelling

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

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
    
    for fn in listdir("cogs/levels"):
        if fn.endswith(".py"):
            bot.load_extension(f"cogs.levels.{fn[:-3]}")
            print(f"Loading cogs.levels.{fn[:-3]}")
    
    for fn in listdir("Addons"):
        if fn.endswith(".py"):
            bot.load_extension(f"Addons.{fn[:-3]}")
            print(f"Loading Addons.{fn[:-3]}")

    bot.load_extension("Systems.levelsys")
    print("Loading Systems.levelsys")

print("Loaded extensions")

@bot.event
async def on_ready():
    print('------')
    print('Logged In As:')
    print(f"Username: {bot.user.name}\nID: {bot.user.id}")
    print('------')
    activity = nextcord.Game(name=config['bot_status_text'])
    config_status = config['bot_status_text']
    config_activity = config['bot_activity']
    await bot.change_presence(status=config_activity, activity=activity)
    for guild in bot.guilds:
        serverstats = levelling.find({"server": guild.id, "ignored_channels": {"$exists": False}})
        for doc in serverstats:
            levelling.update_one({"server": guild.id}, {"$set": {"ignored_channels": []}})
            print(f"Guild: {guild.name} was missing 'ignored_channels' -  Automatically added it!")
        userstats = levelling.find({"guildid": guild.id, "name": {"$exists": False}, "id": {"$exists": True}})
        for doc in userstats:
            member = await bot.fetch_user(doc["id"])
            levelling.update_one({"guildid": guild.id, "id": doc['id']}, {"$set": {"name": str(f"{member}")}})
            print(f"The field NAME was missing for: {member} - Automatically added it!")
    stats = levelling.find_one({"bot_name": f"{bot.user.name}"})
    if stats is None:
        bot_data = {"bot_name": f"{bot.user.name}", "event_state": False}
        levelling.insert_one(bot_data)

@bot.event
async def on_member_join(member):
    try:
        channel = bot.get_channel(config['WELCOME_CHANNEL_ID'])
        rules   = bot.get_channel(config['RULES_CHANNEL'])
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
