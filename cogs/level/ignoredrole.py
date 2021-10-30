import nextcord
from nextcord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
with open("Configs/spamconfig.yml", "r", encoding="utf-8") as file:
    spamconfig = yaml.load(file)

# Spam system class
class ignoredrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #Reset command
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def ignoredrole(self, ctx, role=None):
        if spamconfig['antispam_system'] is True:
            stats = levelling.find_one({"server" : ctx.guild.id})
            if role is None:
                prefix = config['Prefix']
                embed2 = nextcord.Embed(title=f":x: SETUP FAILED",
                                        description=f"You need to enter a valid name!",
                                        color=config['error_embed_color']
                            )
                embed2.add_field(name="Example:", value=f"`{prefix}ignoredrole <role>`")
                await ctx.send(embed=embed2)
            elif role:
                levelling.update_one(
                    {
                        "server" : ctx.guild.id
                    },
                    {
                        "$set" : {
                            "ignoredRole" : str(role)
                        }
                    }
                )
                embed = nextcord.Embed(title=f":white_check_mark: IGNORED ROLE SET!",
                                    description=f"Ignored Role Now: `{role}`",
                                    color=config['success_embed_color']
                        )
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ignoredrole(bot))