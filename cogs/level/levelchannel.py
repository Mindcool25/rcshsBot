import nextcord
from nextcord.ext import commands
from ruamel.yaml import YAML
from Systems.levelsys import levelling

# Reads the config file, no need for changing
yaml = YAML()
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

# Spam system class
class levelchannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Reset command
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def levelchannel(self, ctx, channel=None):
        stats = levelling.find_one({"server" : ctx.guild.id})
        if stats is None:
            newserver = {
                "server" : ctx. guild.id,
                "level_channel" : " "
            }
            levelling.insert_one(newserver)
        else:
            if channel is None:
                prefix = config['Prefix']
                embed2 = nextcord.Embed(title=f":x: SETUP FAILED",
                        description=f"You need to enter a channel name!",
                        color = config['error_embed_color']
                )
                embed2.add_field(name="Example:", value=f"`{prefix}levelchannel <channelname>`\n\n***Please do not use the # and enter any -'s! ({prefix}levelchannel test-channel)***")
                await ctx.send(embed=embed2)
            elif channel:
                levelling.update_one(
                    {
                        "server" : ctx.guild.id
                    },
                    {
                        "$set" : {
                            "level_channel" : channel
                        }
                    }
                )
                embed = nextcord.Embed(title=f":white_check_mark: LEVEL CHANNEL",
                        description=f"The new level channel is: `{channel}`",
                        color=config['success_embed_color']
                )
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(levelchannel(bot))