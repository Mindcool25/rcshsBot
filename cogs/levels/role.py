import nextcord
from nextcord.ext import commands
from pymongo import DESCENDING
from ruamel.yaml import YAML
from Systems.levelsys import levelling
from cogs.levels.levelchannel import levelchannel

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

    prefix = config['Prefix']

# Spam system class
class role(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def role(self, ctx, addorremove=None, level=None, *, role: nextcord.Role = None):
        if addorremove is None:
            embed = nextcord.Embed(title=":x: There was an Error!", description=f"`{prefix}role <add|remove> <level> <role>`")
            await ctx.send(embed=embed)
            return
        
        if level is None:
            embed = nextcord.Embed(title=":x: There was an Error!", description=f"`{prefix}role <add|remove> <level> <role>`")
            await ctx.send(embed=embed)
            return
        
        if role is None:
            embed = nextcord.Embed(title=":x: There was an Error!", description=f"`{prefix}role <add|remove> <level> <role>`")
            await ctx.send(embed=embed)
            return
        
        if addorremove.lower() == "add":
            if level:
                serverstats = levelling.find_one({"server": ctx.guild.id})
                if role in ctx.guild.roles:
                    if role.name in serverstats['role']:
                        embed = nextcord.Embed(title=":x: That role can already be unlocked", description=f"`{prefix}role <add|remove> <level> <role>")
                        await ctx.send(embed=embed)
                        return
                
                    else:
                        levelling.update_one({"server": ctx.guild.id}, {"$push": {"role": role.name, "level": level}})
                        embed = nextcord.Embed(title=f":white_check_mark: Added `{role.name}` to unlock at Level `{level}`")
                        await ctx.send(embed=embed)
                        return
        
                else:
                    embed = nextcord.Embed(title=":x: That role doesnot exist", description=f"`{prefix}role <add|remove> <level> <role>`")
                    await ctx.send(embed=embed)
                    return
        
        if addorremove.lower() == "remove":
            serverstats = levelling.find_one({"server": ctx.guild.id})
            if role.name in serverstats['role']:
                levelling.update_one({"server": ctx.guild.id}, {"$pull": {"role": role.name, "level": level}})
                embed = nextcord.Embed(title=f":white_check_mark: Removed `{role.name}` from unlocking at Level `{level}`")
                await ctx.send(embed=embed)
                return
            else:
                embed = nextcord.Embed(title=":x: That role cannot be unlocked!")
                await ctx.send(embed=embed)
                return

    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx):
        serverstats = levelling.find_one({"server": ctx.guild.id})
        embed = nextcord.Embed(title="🔓 // LEVEL ROLES", description=f"Level Roles for `{ctx.guild.name}`")
        if len(serverstats['role']) < 1:
            embed.add_field(name="Roles:", value="`There are no roles to unlock!`")
            embed.add_field(name="Level:", value="`No level required!`")
        else:
            embed.add_field(name="Roles:", value=f"`{str(serverstats['role']).replace('[', '').replace(']', '')}`")
            embed.add_field(name="Level:", value=f'`{str(serverstats["level"]).replace("[", "").replace("]", "")}`')
        await ctx.send(embed=embed)


# Sets-up the cog for help
def setup(client):
    client.add_cog(role(client))