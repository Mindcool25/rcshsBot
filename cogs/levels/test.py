
from nextcord.ext import commands
from ruamel.yaml import YAML
from Libs.get import *
from Libs.getServer import *
from Libs.set import *

yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class config(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Leaderboard Command
    @commands.command()
    @commands.guild_only()
    async def test(self, ctx, member: nextcord.Member = None):
        # embed
        if member is None:
            member = ctx.author
        xp_color = getXPColor(id=member.id, guildID=ctx.guild.id)
        color_xp = await xp_color
        without_tag = color_xp.replace("#", '')
        embed = nextcord.Embed(title=f"TEST | USER | {member.name}", color=int(f"0x{without_tag}", 0))

        level = getLevel(id=member.id, guildID=ctx.guild.id)
        embed.add_field(name="Level:", value="`" + str(await level) + "`")

        xp = getXP(id=member.id, guildID=ctx.guild.id)
        embed.add_field(name="XP:", value="`" + str(await xp) + "`")

        embed.add_field(name="XP color:", value="`" + str(color_xp) + "`")

        circle = getCirlce(id=member.id, guildID=ctx.guild.id)
        embed.add_field(name="Circle Pic?:", value="`" + str(await circle) + "`")

        background = backgroundUrl(id=member.id, guildID=ctx.guild.id)
        embed.set_image(url=str(await background))

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def server(self, ctx):
        xp_color = getXPColor(id=ctx.author.id, guildID=ctx.guild.id)
        color_xp = await xp_color
        without_tag = color_xp.replace("#", '')
        embed = nextcord.Embed(title=f"TEST | SERVER | {ctx.guild.name}", color=int(f"0x{without_tag}", 0))
        xp = xpPerMessage(guildID=ctx.guild.id)
        embed.add_field(name="XP/Message:", value='`' + str(await xp) + '`')
        double_xp = doubleXPRole(guildID=ctx.guild.id)
        embed.add_field(name="x2 XP Role:", value='`' + str(await double_xp) + '`')
        level_channel = levelChannel(guildID=ctx.guild.id)
        embed.add_field(name="Level Channel: ", value='`#' + str(await level_channel) + '`')
        levels = getLevels(guildID=ctx.guild.id)
        embed.add_field(name="Levels for Roles:", value='`' + str(await levels) + '`')
        roles = getRoles(guildID=ctx.guild.id)
        embed.add_field(name="Roles for Levels:", value='`' + str(await roles) + '`')
        ignored_role = ignoredRole(guildID=ctx.guild.id)
        embed.add_field(name="Ignored Role:", value='`' + str(await ignored_role) + '`')
        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def setxp(self, ctx, amount=None):
        if amount is None:
            await ctx.send("amount not set")
        await setXP(id=ctx.author.id, guildID=ctx.guild.id, amount=amount)
        await ctx.send(f"Set <@{ctx.author.id}>'s xp to {amount}xp ")

    @commands.command()
    @commands.guild_only()
    async def setbackground(self, ctx, link=None):
        if link is None:
            await ctx.send("amount not set")
        await setBackground(id=ctx.author.id, guildID=ctx.guild.id, link=link)
        await ctx.send(f"Set <@{ctx.author.id}>'s background to {link}")

    @commands.command()
    @commands.guild_only()
    async def setxpcolor(self, ctx, hex_code=None):
        if hex is None:
            await ctx.send("hex not set")
        await setXPColor(id=ctx.author.id, guildID=ctx.guild.id, hex_code=hex_code)
        await ctx.send(f"Set <@{ctx.author.id}>'s xp color to {hex_code}")

    @commands.command()
    @commands.guild_only()
    async def setcircle(self, ctx, state=None):
        if hex is None:
            await ctx.send("state not set")
        await setCircle(id=ctx.author.id, guildID=ctx.guild.id, value=state)
        await ctx.send(f"Set <@{ctx.author.id}>'s xp color to {state}")


# Sets-up the cog for help
def setup(client):
    client.add_cog(config(client))
