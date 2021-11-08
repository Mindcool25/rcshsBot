import nextcord
from nextcord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


# Spam system class
class doublexp(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Reset Command
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def doublexp(self, ctx, *, role=None):
        stats = levelling.find_one({"server": ctx.guild.id})
        if stats is None:
            newserver = {"server": ctx.guild.id, "double_xp_role": " "}
            levelling.insert_one(newserver)
        else:
            if role is None:
                prefix = config['Prefix']
                embed2 = nextcord.Embed(title=f":x: SETUP FAILED",
                                       description=f"You need to enter a role name!",
                                       color=config['error_embed_color'])
                embed2.add_field(name="Example:", value=f"`{prefix}doublexp <rolename>`")
                await ctx.send(embed=embed2)
            elif role:
                levelling.update_one({"server": ctx.guild.id}, {"$set": {"double_xp_role": role}})
                embed = nextcord.Embed(title=f":white_check_mark: DOUBLE XP ROLE!", description=f"The new Double XP Role: `{role}`",
                                      color=config['success_embed_color'])
                await ctx.send(embed=embed)


# Sets-up the cog for help
def setup(client):
    client.add_cog(doublexp(client))