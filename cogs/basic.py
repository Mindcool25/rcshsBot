# Using cogs makes life a lot easier.
import discord
from discord.ext import commands
from datetime import datetime as d


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
		start = d.timestamp(d.now)
		print("pinging...")
		msg = await ctx.send(content="Pinging...")  # Sending initial message
		await msg.edit(
			content=f'Pong!\nOne message round-trip took {(d.timestamp(d.now()) - start) * 1000}ms.')  # Editing message
		return

	# Basic echo command to show how you can get input from user
	@commands.command(
		name="echo",
		description="Command to echo what a user puts in",
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
