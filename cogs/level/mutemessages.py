import nextcord
from nextcord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Read the config files
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)
with open("Configs/spamconfig.yml", "r", encoding="utf-8") as file:
    spamconfig = yaml.load(file)

# Spam system class
class mutemessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def mutemessages(self, ctx, amount=None):
        if spamconfig['antispam_system'] is True:
            stats = levelling.find_one({"server" : ctx.guild.id})
            if amount is None:
                prefix = config['Prefix']
                embed2 = nextcord.Embed(title=f":x: SETUP FAILED",
                                    description=f"You need to enter a valid integer!",
                                    color=config['error_embed_color']
                )
                embed2.add_field(name="Example:", value=f"`{prefix}mutemessages <amount>`")
                await ctx.send(embed=embed2)
            elif amount:
                levelling.update_one(
                    {
                        "server" : ctx.guild.id
                    },
                    {
                        "$set" : {
                            "muteMessages" : int(amount)
                        }
                    }
                )
                embed = nextcord.Embed(title=f":white_check_mark: MUTE MESSAGES SET!", description=f"Mute Messages Now: `{amount}`",
                                        color=config['success_embed_color'])
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(mutemessages(bot))