import botPrefixes as bp
import nextcord
from nextcord.ext import commands

async def print_prefixes(ctx):
  tempPres = ""
  for i in range(len(bp.prefixes)):
    tempPres += f"<{bp.prefixes[i]}> "
  await ctx.reply(f"Your prefixes are: {tempPres}")

class PrefixCog(commands.Cog, command_attrs=dict(has_guild_permissions="Administrator")): #command_attrs allows you to add cog wide command attributes
  #Initialise the bot
  def __init__(self, bot):
	  self.bot = bot 


  # command to change a single prefix
  @commands.command(
    name="changePrefix",
    description="Change a single prefix.",
    usage=f" <prefix to change> <new prefix>",
    aliases=['cp']
  )
  async def change_single_prefix(self, ctx, changePrefix, newPrefix):
    bp.prefixes.remove(changePrefix)
    bp.prefixes.append(newPrefix)
    await print_prefixes(ctx)


  # command to remove all prefixes and assign a new one
  @commands.command(
    name="removeAllPrefixes",
    description="This will remove all of the current prefixes and set a new one.",
    usage=f"{bp.prefixes} <new prefix>",
    aliases=["rap"]
  )
  async def remove_all_prefixes(self, ctx, newPrefix:str):
    bp.prefixes.clear()
    print(bp.prefixes)
    bp.prefixes.append(newPrefix)
    await print_prefixes(ctx)


  # command to remove a single prefix
  @commands.command(
    name="removeSinglePrefix",
    description="Removes the specified prefix.",
    usage=f"{bp.prefixes} <prefix to remove>",
    aliases=['rsp']
  )
  async def remove_single_prefix(self, ctx, removePrefix):
    if len(bp.prefixes) > 0:  
      bp.prefixes.remove(removePrefix)
      await print_prefixes(ctx)
    else:
      await ctx.reply("Please add another prefix before removing this one.")


  # command to list all current prefixes
  @commands.command(
    name="listPrefixes",
    description="Shows all the prefixes you can use for the bot.",
    aliases=["lp"]
  )
  async def list_prefixes(self, ctx):
    await print_prefixes(ctx)


  # command to add a new prefix
  @commands.command(
    name="addPrefix",
    desscription="Adds a new prefix to the bot.",
    usage=f" <new prefix>",
    aliases=["ap"]
  )
  async def add_prefix(self, ctx, newPrefix):
    for i in bp.prefixes:
      if i == newPrefix:
        await ctx.reply("This is already a prefix.")
        return
    bp.prefixes.append(str(newPrefix))
    await print_prefixes(ctx)

def setup(bot):
	bot.add_cog(PrefixCog(bot))