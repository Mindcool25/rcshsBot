import re

import nextcord
from nextcord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Background Command
    @commands.command()
    @commands.guild_only()
    async def background(self, ctx, link=None):

        if link:
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"background": f"{link}"}})
            embed = nextcord.Embed(title=":white_check_mark: BACKGROUND CHANGED!")
            embed.set_thumbnail(url=link)
            await ctx.channel.send(embed=embed)

        elif link is None:
            embed3 = nextcord.Embed(title=":x: SOMETHING WENT WRONG!", description="`Link was not defined!`")
            await ctx.channel.send(embed=embed3)

    # XP-COLOUR Command
    @commands.command()
    @commands.guild_only()
    async def xpcolour(self, ctx, colour=None):
        if colour is None:
            embed = nextcord.Embed(description=":x: Incorrect Hex value entered.")

            await ctx.send(embed=embed)

        else:

            x = re.search("#", colour)
            if x:
                if len(colour) == 7:
                    levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"xp_colour": f"{colour}"}})

                    colour_without_tag = colour.replace('#', '')

                    embed = nextcord.Embed(title=":white_check_mark: Colour set successfully!", colour=int(f"0x{colour_without_tag}", 0))

                    await ctx.send(embed=embed)
                else:
                    embed = nextcord.Embed(title=":x: Incorrect Hex value entered.")

                    await ctx.send(embed=embed)

            else:
                embed = nextcord.Embed(title=":x: Incorrect Hex value entered.")

                await ctx.send(embed=embed)

    # CIRCLE-PIC Command
    @commands.command()
    @commands.guild_only()
    async def circlepic(self, ctx, value=None):
        await ctx.message.delete()
        if value == "True":
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"circle": True}})
            embed1 = nextcord.Embed(title=":white_check_mark: PROFILE CHANGED!")
            await ctx.channel.send(embed=embed1)
        elif value == "False":
            levelling.update_one({"guildid": ctx.guild.id, "id": ctx.author.id}, {"$set": {"circle": False}})
            embed2 = nextcord.Embed(title=":white_check_mark: PROFILE CHANGED!")

            await ctx.channel.send(embed=embed2)
        elif value is None:
            embed3 = nextcord.Embed(title=":x: SOMETHING WENT WRONG!")
            await ctx.channel.send(embed=embed3)

# Sets-up the cog for Profile+
def setup(client):
    client.add_cog(Profile(client))
