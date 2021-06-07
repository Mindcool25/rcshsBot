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
	# Function for ping command
	async def ping_command(self, ctx):  # Async is used to make sure the bot is running correctly without timing issues
		start = d.timestamp(d.now())
		print("pinging...")
		msg = await ctx.send(content="Pinging...")  # Sending initial message
		await msg.edit(
			content=f'Pong!\nOne message round-trip took {(d.timestamp(d.now()) - start) * 1000}ms.')  # Editing message
		return

	# Basic echo command to show how you can get input from user
	@commands.command(
		name="echo",
		description="Command to echo what a user puts in",
		usage=".echo <phrase to echo>",
		aliases=['e']
	)
	# Function for echo
	async def echo_command(self, ctx):
		# Getting rid of prefix and the characters used to invoke the command
		userInput = ctx.message.content
		userInput = userInput[len(ctx.prefix) + len(ctx.invoked_with):]
		userInput = userInput[1:]
		# Sending what the user typed back
		msg = await ctx.send(content=userInput)
		return
		# Basic command to show github link to the bot in chat
	@commands.command(
		name="github",
		description="Command to show github link to bot",
		usage=".github",
		aliases=['g']
	)	
		# Function for github
	async def github_command(self, ctx):
		# Send our github link in chat
		msg = await ctx.send("https://github.com/Mindcool25/rcshsBot")
		return


	# Sends github link
	@commands.command(
		name="github",
		description="Send link to the bot github",
		usage="just do .github its not that hard",
		aliases=['gh'])
	async def github_command(self, ctx):
		async ctx.send("https://github.com/Mindcool25/rcshsBot")
	
	
#ALWAYS KEEP THIS HERE
# This needs to be at the bottom of all cog files for the cog to be added to the main bot
def setup(bot):
	bot.add_cog(BasicCog(bot))
