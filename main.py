#IMPORTS
import nextcord
from nextcord.activity import Activity
import botPrefixes as bp
from nextcord.ext import commands

WELCOME_MESSAGE_ID  = 846940613478973453
RULES_CHANNEL       = 848980735754240040

#NOT TO BE EDITED!
with open("token.txt") as f:
    TOKEN = f.readline()

def get_prefix(bot, message):
    return commands.when_mentioned_or(*bp.prefixes)(bot, message)

bot = commands.Bot(
    command_prefix=get_prefix,
    description="Bot for the r/CSHighschoolers discord server",
    intents=nextcord.Intents.all()
)

bot.remove_command('help')

# If you make your own cog file, add it in a similar way that basic is added here, with 'cogs.<filename>'
extensions = ["cogs.basic","cogs.music", "cogs.utils.prefix_control", "cogs.reddit", "cogs.utils.help"]

if __name__ == "__main__":
    for extension in extensions:
        print(f"Loading {extension}...")
        bot.load_extension(extension)
print("Loaded extensions")

@bot.event
async def on_ready():
    print("Logged in as", bot.user.name)
    # await bot.change_presence(nextcord.Activity(type=nextcord.ActivityType.listening(name="Closer")))

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
