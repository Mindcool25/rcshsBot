#IMPORTS
import nextcord
from nextcord.activity import Activity
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound, MissingRequiredArgument, CommandInvokeError, MissingRole, NoPrivateMessage
import botPrefixes as bp
from ruamel.yaml import YAML
import logging
import os
from os import listdir

from Systems.levelsys import levelling

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
with open("Configs/spamconfig.yml", "r", encoding="utf-8") as file2:
    spamconfig = yaml.load(file2)

#NOT TO BE EDITED!
with open("token.txt") as f:
    TOKEN = f.readline()

def get_prefix(bot, message):
    return commands.when_mentioned_or(*bp.prefixes)(bot, message)

bot = commands.Bot(
    command_prefix=get_prefix,
    description="Bot for the r/CSHighschoolers discord server",
    intents=nextcord.Intents.all(),
    case_insensitive=True
)

bot.remove_command('help')


# sends discord logging files which could potentially be useful for catching errors.
os.remove("Logs/logs.txt")
FORMAT = '[%(asctime)s]:[%(levelname)s]: %(message)s'
logging.basicConfig(filename='Logs/logs.txt', level=logging.DEBUG, format=FORMAT)
logging.debug('Started Logging')
logging.info('Connecting to Discord.')

# If you make your own cog file, add it in a similar way that basic is added here, with 'cogs.<filename>'
extensions = ["cogs.basic","cogs.music", "cogs.utils.prefix_control", "cogs.reddit", "cogs.utils.help"]

if __name__ == "__main__":
    for extension in extensions:
        print(f"Loading {extension}...")
        bot.load_extension(extension)
print("Loaded extensions")

@bot.event
async def on_ready():
    config_status = config['bot_status_text']
    config_activity = config['bot_activity']
    activity = nextcord.Game(name=config['bot_status_text'])
    logging.info('Getting Bot Activity from Config')
    print("If you encounter any bugs, please let me know.")
    print('------')
    print('Logged In As:')
    print(f"Username: {bot.user.name}\nID: {bot.user.id}")
    print('------')
    print(f"Status: {config_status}\nActivity: {config_activity}")
    print('------')
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

@bot.command()
async def addons(ctx):
    # ✅ // ❌
    embed = nextcord.Embed(title="ADDON PACKAGES")

    # Clan System
    if os.path.exists("Addons/Clan System.py") is True:
        embed.add_field(name="Clan System", value="`Installed ✅`")
    else:
        embed.add_field(name="Clan System", value="`Installed ❌`")

    # Holiday System
    if os.path.exists("Addons/Holiday System.py") is True:
        embed.add_field(name="Holiday System", value="`Installed ✅`")
    else:
        embed.add_field(name="Holiday System", value="`Installed ❌`")

    # Vocal System
    if os.path.exists("Addons/Vocal System.py") is True:
        embed.add_field(name="Vocal System", value="`Installed ✅`")
    else:
        embed.add_field(name="Vocal System", value="`Installed ❌`")

    # Profile+
    if os.path.exists("Addons/Profile+.py") is True:
        embed.add_field(name="Profile+", value="`Installed ✅`")
    else:
        embed.add_field(name="Profile+", value="`Installed ❌`")

    # Extras+
    if os.path.exists("Addons/Extras+.py") is True:
        embed.add_field(name="Extras+", value="`Installed ✅`")
    else:
        embed.add_field(name="Extras+", value="`Installed ❌`")

    # Stats
    if os.path.exists("Addons/Stats.py") is True:
        embed.add_field(name="Stats", value="`Installed ✅`")
    else:
        embed.add_field(name="Stats", value="`Installed ❌`")

    # Events
    if os.path.exists("Addons/Events.py") is True:
        embed.add_field(name="Events", value="`Installed ✅`")
    else:
        embed.add_field(name="Events", value="`Installed ❌`")

    await ctx.send(embed=embed)

logging.info("------------- Loading -------------")
for fn in listdir("Commands"):
    if fn.endswith(".py"):
        logging.info(f"Loading: {fn}")
        bot.load_extension(f"Commands.{fn[:-3]}")
        logging.info(f"Loaded {fn}")

for fn in listdir("Addons"):
    if fn.endswith(".py"):
        logging.info(f"Loading: {fn} Addon")
        bot.load_extension(f"Addons.{fn[:-3]}")
        logging.info(f"Loaded {fn} Addon")

logging.info(f"Loading Level System")
bot.load_extension("Systems.levelsys")
logging.info(f"Loaded Level System")

if spamconfig['antispam_system'] is True:
    logging.info(f"Loading Anti-Spam System")
    bot.load_extension("Systems.spamsys")
    logging.info(f"Loaded Anti-Spam System")

logging.info("------------- Finished Loading -------------")

"""
This will handle events but if you dont handle every single error you can get, some might slip by without you knowing.
For more info watch (https://youtu.be/_2ifplRzQtM?list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ)
"""
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.reply("Please pass in all required arguments.")

bot.run(TOKEN, reconnect=True)
