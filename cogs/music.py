# Using cogs makes life a lot easier!
import nextcord
from nextcord import voice_client
from nextcord import file
from nextcord.ext import commands
from datetime import datetime as d
import os
from nextcord.member import M
from nextcord.player import FFmpegAudio
import youtube_dl
import asyncio

# Initialization
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
	'format' : 'bestaudio/best',
	'restrictfilenames' : True,
	'noplaylist' : True,
	'nocheckcertificate' : True,
	'ignoreerrors' : False,
	'logtostderr' : False,
	'quiet' : True,
	'no_warnings' : True,
	'default_search' : 'auto',
	'source_address' : '0.0.0.0' # bind to ipv4 since ipv6 can cause issues sometimes
}

ffmpeg_options = {
	'options' : '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(nextcord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume = 0.5):
		super().__init__(source, volume)
		self.data = data
		self.title = data.get('title')
		self.url = ""
	
	@classmethod
	async def from_url(cls, url, *, loop = None, stream = False):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
		if 'enteries' in data:
			# take first item from the playlist
			data = data['enteries'][0]
		filename = data['title'] if stream else ytdl.prepare_filename(data)
		return filename

class MusicCog(commands.cog):
	# Initializing cog into the bot
	def __init__(self, bot):
		self.bot = bot

	# Command to join voice channel
	@commands.command(
		name="join",
		description="Command to connect to voice channel",
		usage=".join",
		aliases=['j']
	)
	async def join(ctx):
		if not ctx.message.author.voice:
			await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
			return
		else:
			channel = ctx.message.author.voice.channel
		await channel.connect()

	# Command to leave voice channel
	@commands.command(
		name="leave",
		description="Command to disconnect from voice channel",
		usage=".leave",
		aliases=['l']
	)
	async def leave(ctx):
		voice_client = ctx.message	
		if voice_client.is_connected():
			await voice_client.disconnect()
		else:
			await ctx.send("This bot is not connected to the voice channel")

	# Command to play music
	@commands.command(
		name="play",
		description="Command to play music from url",
		usage=".play <url>",
		aliases=['p']
	)
	async def play(ctx, url):
		try:
			server = ctx.message.guild
			voice_channel = server.voice_client

			async with ctx.typing():
				filename = await YTDLSource.from_url(url, loop=commands.loop)
				voice_channel.play(nextcord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
			await ctx.send('**Now Playing:** {}'.format(filename))
		except:
			await ctx.send("The bot is not connected to a voice channel")
	
	# Command to pause music
	@commands.command(
		name="pause",
		description="Command to pause music",
		usage=".pause",
		aliases=['pa']
	)
	async def pause(ctx):
		voice_client = ctx.message.guild.voice_client
		if voice_client.is_playing():
			await ctx.pause()
		else:
			await ctx.send("The bot is not playing anything at the moment")
	
	# Command to resume music
	@commands.command(
		name="resume",
		description="Command to resume music",
		usage=".resume",
		aliases=['r']
	)
	async def resume(ctx):
		voice_client = ctx.message.guild.voice_client
		if voice_client.is_paused():
			await ctx.resume()
		else:
			await ctx.send("The bot wasn't playing anything before this. Use play command")
	
	# Command to stop music
	@commands.command(
		name="stop",
		description="Command to stop music",
		usage=".stop",
		aliases=['s']
	)
	async def stop(ctx):
		voice_client = ctx.message.guild.voice_client
		if voice_client.is_playing():
			await ctx.stop()
		else:
			await ctx.send("The bot isn't playing anything at the moment")

#ALWAYS KEEP THIS HERE
# This needs to be at the bottom of all cog files for the cog to be added to the main bot
def setup(bot):
	bot.add_cog(MusicCog(bot))
