# Using cogs makes life a lot easier!
import discord
from discord.ext import commands
from datetime import datetime as d



# THIS IS THE OFFICIAL BOT OF r/CSHIGHSCHOOLERS. 
# If you have an idea for the bot, you're supposed to be editing this file.
# Write REALLY neat code and don't mess with the main.py file in the repository. 
# Also don't mess with the commands you DON'T want to edit. 
# Make sure your code is neat and understandable so it can be checked and your feature will be up in NO TIME!
# If you feel like your command is better suited for another file or plan on making a series of similar/connected commands, making a new cog file like this one would be preferrable. Make sure you read the comments on this file to understand how to make your own.
# Thank you for contributing! 

invite_code = "q5S9jCgzP6"


#COMMMANDS!
class BasicCog(commands.Cog):
	# Initializing cog into the bot
	def __init__(self, bot):
		self.bot = bot

	# Basic ping command to get bot response speed
	@commands.command(
		name="ping",  # The name of the command, what you will type to invoke the command
		description="Command to get how fast the bot responds to a command.",  # Description for help command
		aliases=['p']  # This allows you to have a shorthand for a command or just call it something different
	)
	async def ping_command(self, ctx):
		start = d.timestamp(d.now())
		print("Pinging...")
		msg = await ctx.send(content="Pinging...")  # Sending initial message
		await msg.edit(
			content=f'Pong!\nOne message round-trip took {(d.timestamp(d.now()) - start) * 1000}ms.')

	# Basic echo command to show how you can get input from user
	@commands.command(
		name="echo",
		description="Command to echo what a user puts in",
		usage=".echo <phrase to echo>",
		aliases=['e']
	)
	async def echo_command(self, ctx, text: str):
		if (text == "@everyone" or text == "@member"):
			return
		else: await ctx.send(text)
		
	# Respond with the github repo link
	@commands.command(
		name="github",
		description="Command to show github link to bot",
		usage=".github",
		aliases=['g']
	)	
	async def github_command(self, ctx):
		await ctx.message.reply("https://github.com/Mindcool25/rcshsBot", mention_author=True)
		
	# Basic command to show discord invite link
	@commands.command(
		name="invite",
		description="Command to show discord server invite link",
		usage=".invite",
		aliases=['i']
	)	
	async def invite_command(self, ctx):
		# Send our discord invite link in chat
		invites = await ctx.guild.invites()
		active_codes = [i.code for i in invites]
		if invite_code not in active_codes:
			await ctx.message.reply("The currently set invite code is no longer valid!", mention_author=True)
		else:
			await ctx.message.reply(f"https://discord.gg/{invite_code}", mention_author=True)
	
	# Basic command to send a link to the associated subreddit with a reply
	@commands.command( 
        	name='subreddit',
        	description="Get the link to the subreddit",
        	usage=".subreddit",
        	aliases=['sr','sub','reddit','r']
    	)
    	async def subreddit_command(self, ctx):
        	# Assuming you're using the most up-to-date d.py,
        	await ctx.message.reply("Check out the subreddit here: https://www.reddit.com/r/cshighschoolers/", mention_author=True)
		
#ALWAYS KEEP THIS HERE
# This needs to be at the bottom of all cog files for the cog to be added to the main bot
def setup(bot):
	bot.add_cog(BasicCog(bot))
