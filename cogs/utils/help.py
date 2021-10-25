import nextcord
from nextcord.ext import commands
from nextcord.errors import Forbidden
import botPrefixes

"""
This custom help command is a perfect replacement for the default one on any Discord Bot written in Discord.py!
However, you must put "bot.remove_command('help')" in your bot, and the command must be in a cog for it to work.
"""

async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    -  tries to send embed in channel
    -  tries to send normal message when that fails
    -  tries to send embed private with information about missing information about missing permissions
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions!")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue?", embed=embed
            )

class Help(commands.Cog):
    """Sends this help message"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    # @commands.bot_has_perimissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *input):
        """Help?!"""
        
        # CONFIGURATION
        prefix      = '$'
        version     = "1.0.5"

        owner       = ""
        owner_name  = ""

        # Checks if cog parameter was given
        # If not: sending all modules and commands not associated with a cog
        if not input:
            # checks if owner is on this server - sed to 'tag' owner
            try:
                owner = ctx.guild.get_membet(owner).mention
            
            except AttributeError as e:
                owner = owner
            
            # starting to build embed
            emb = nextcord.Embed(title='Commands and modules', color=nextcord.Color.blue(),
            description=f"Use `{prefix}help <module>` to gain more information about that module\n"
            )

            # iterating through cogs, gathering descriptions
            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}`\n{self.bot.cogs[cog].__doc__}\n\n'

            # adding 'list' of cogs to embed
            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            # integrating through uncategorized commands
            commands_desc = ''
            for command in self.bot.walk_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # adding those commands to embed
            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            # setting information about author
            emb.add_field(name="About", value=f"The Bot is a maintained fork of the original r/cshighschoolers bot developed by Mindcool, based on discord.py.\nPlease visit https://github.com/nuke886/rcshsBot to submit ideas or bugs.")
            
            emb.set_footer(text=f"Bot is running {version}")
        
        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(input) == 1:
            
            # iterating through cogs
            for cog in self.bot.cogs:
                # check if cog is the matching one
                if cog.lower() == input[0].lower():

                    # making title - getting description from doc-string below class
                    emb = nextcord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__, color=nextcord.Color.green())

                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    # found cog - breaking loop
                    break
                
                # if input not found
                # yes, for-loops an else statement, it's called when no 'break' was issued
                else:
                    emb = nextcord.Embed(title="What's that?!",
                    description=f"I've never heard from a module called `{input[0]}` before",
                    color=nextcord.Color.orange())
        
        # too many cogs requested - only one at a time is allowed
        elif len(input) > 1:
            emb = nextcord.Embed(title="That's too much.",
            description="Please request only one module at once",
            color=nextcord.Color.orange())
        
        else:
            emb = nextcord.Embed(title="It's a magical place.",
            description="I don't know how you got here. But I didn't see this coming at all.\n"
                        "Would you please be so kind to report that issue to us on github?\n"
                        "https://github.com/nuke886/rcshsBot\n"
                        "Thank you!",
                        color=nextcord.Color.red()
                    )
        
        # sending reply embed using our own function defined above   
        await send_embed(ctx, emb)

def setup(bot):
    bot.add_cog(Help(bot))