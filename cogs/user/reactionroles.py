from nextcord import RawReactionActionEvent
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.errors import NoEntryPointError

from Configs.reaction_roles import reaction_roles

class ReactionRoles(commands.Cog):
    
    # Initialize the bot
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(
        name="verify",
        description="Send verfiy message",
        aliases=['v'],
        pass_context=True,
        usage=".verify"
    )
    async def verify(self, ctx):
        verify = self.bot.get_channel(848985486324006962)
        embed = nextcord.Embed(description="React with ✅ to get access to the server", color=0x00ff80)
        msg = await verify.send(embed=embed)

        await msg.add_reaction('✅')        

    # Send reaction role message
    @commands.has_permissions(administrator=True)
    @commands.command(
        name="rolemsg",
        description="Send Self roles message",
        aliases=['s'],
        pass_context=True,
        usage=".rolemsg"
    )
    async def rolemsg(self, ctx):
        roles = self.bot.get_channel(848991838903861298)
        
        # Programming Language
        embed = nextcord.Embed(color=0x620fd6)
        embed.add_field(
                name="Languages",
                value="""
React with <:python:848992841153511436> to get <@&848986453274918972> role
React with <:java:848993181911875635> to get <@&848986920456552469> role
React with <:c_:849684521901097031> to get <@&849658650607747112> role
React with <:javascript:848997634026635285> to get <@&848989278587322449> role
React with <:csharp:849683642857947186> to get <@&849658829011419208> role
React with <:html:848998130078842930> to get <@&848995354481000459> role
React with <:rust:905827671399874591> to get <@&856987252462977047> role
React with <:lua:894591276744323182> to get <@&894591574653169705> role
React with <:julia:894595692297867314> to get <@&894595094714384464> role
                    """
        )

        # Grade
        embed2 = nextcord.Embed(color=0xeb5031)
        embed2.add_field(
                name="Grade",
                value="""
React with :one: to get the <@&848993097153380402> role
React with :two: to get the <@&848993822021255198> role
React with :three: to get the <@&848994164611350589> role
React with :four: to get the <@&848994020994842664> role
React with :five: to get the <@&848994304029622312> role
                    """
        )

        # Send messages
        message = await roles.send(embed=embed)
        message2 = await roles.send(embed=embed2)

        emoji = ['<:python:848992841153511436>', '<:java:848993181911875635>', '<:c_:849684521901097031>', '<:javascript:848997634026635285>',
                '<:csharp:849683642857947186>', '<:html:848998130078842930>', '<:rust:905827671399874591>', '<:lua:894591276744323182>', '<:julia:894595692297867314>']
        emoji2 = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        
        for emoji in emoji:
            await message.add_reaction(emoji)
        
        for emoji in emoji2:
            await message2.add_reaction(emoji)

    async def process_reaction(self, payload: RawReactionActionEvent, r_type=None) -> None:
        if payload.message_id in reaction_roles.keys():
            for obj in reaction_roles[payload.message_id]:
                if obj[0] == str(payload.emoji):
                    guild = self.bot.get_guild(payload.guild_id)
                    user = await guild.fetch_member(payload.user_id)
                    role = guild.get_role(obj[1])
                    if role is None:
                        print("Invalid role")
                    elif r_type == "add":
                        await user.add_roles(role)
                    elif r_type == "remove":
                        await user.remove_roles(role)
                    else:
                        self.bot.warn("Invalid Reaction type")
                    break
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        await self.process_reaction(payload, "add")
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        await self.process_reaction(payload, "remove")

def setup(bot):
    bot.add_cog(ReactionRoles(bot))