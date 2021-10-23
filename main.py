#IMPORTS
import nextcord
import botPrefixes as bp
from nextcord.ext import commands
import asyncio

#NOT TO BE EDITED!
with open("token.txt") as f:
    TOKEN = f.readline()

def get_prefix(bot, message):
    return commands.when_mentioned_or(*bp.prefixes)(bot, message)


# intents = nextcord.Intents.default()
# intents.members = True

# If you make your own cog file, add it in a similar way that basic is added here, with 'cogs.<filename>'
extensions = ["cogs.basic","cogs.music", "cogs.moderation.prefix_control"]

bot = commands.Bot(
    command_prefix=get_prefix, description="Bot for the r/CSHighschoolers discord server")

if __name__ == "__main__":
    for extension in extensions:
        print(f"Loading {extension}...")
        bot.load_extension(extension)
print("Loaded extensions")

@bot.event
async def on_member_join(member):
    for guild in bot.guilds:
         for channel in guild.text_channels:
             if str(channel) == "👋-welcome":
                await channel.send(f"Welcome {member.mention} to r/cshighschoolers' discord server. Check out our rules over at #848980735754240040 and have a nice stay!")

# @bot.event
# async def on_ready():
#     for guild in bot.guilds:
#         for channel in guild.text_channels:
#             if str(channel) == "🌎-general" or str(channel) == "𝕋𝕒𝕝𝕜𝕤":
#                 Embed = nextcord.Embed()
#                 Embed.set_image(url="https://c.tenor.com/Fi1DbctJXQQAAAAC/what-what-up.gif")
#                 await channel.send(embed=Embed)
#         print(f"Active in {guild.name}\n Member Count : {guild.member_count}")

# This will handle events but if you dont handle every single error you can get, some might slip by without you knowing.
# For more info watch (https://youtu.be/_2ifplRzQtM?list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ)
# 
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.reply("Please pass in all required arguments.")

bot.run(TOKEN, reconnect=True)