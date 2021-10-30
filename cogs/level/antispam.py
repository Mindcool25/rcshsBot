import nextcord
from nextcord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need to changing.
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
with open("Configs/spamconfig.yml", "r", encoding="utf-8") as file:
    spamconfig = yaml.load(file)

# Spam system class
class antispam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def antispam(self, ctx, state=None):
        if spamconfig['antispam_system'] is True:
            stats = levelling.find_one({"server" : ctx.guild.id})
            if state is None:
                prefix = config['Prefix']
                embed2 = nextcord.Embed(title=f":x: SETUP FAILED",
                                description=f"You need to enter a valid state!",
                                color=config['error_embed_color']
                )
                await ctx.send(embed=embed2)
            elif state.lower == "true":
                levelling.update_one(
                    {
                        "server" : ctx.guild.id
                    },
                    {
                        "$set" : {
                            "Antispam" : True
                        }
                    }
                )
                embed = nextcord.Embed(title=f":white_check_mark: ANTISPAM ENABLED!", description=f"Anti-Spam now set to: `{state}`",
                                        color=config['success_embed_color'])
                await ctx.send(embed=embed)
            elif state.lower == "false":
                levelling.update_one(
                    {
                        "server" : ctx.guild.id
                    },
                    {
                        "$set" : {
                            "Antispam" : False
                        }
                    }
                )
                embed = nextcord.Embed(title=f":white_check_mark: ANTISPAM DISABLED!", description=f"Anti-Spam now set to: `{state}`",
                                        color=config['success_embed_color'])
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(antispam(bot))