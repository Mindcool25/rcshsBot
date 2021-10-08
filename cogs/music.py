import nextcord
from nextcord.ext import commands
from nextcord.flags import alias_flag_value
from nextcord.player import FFmpegPCMAudio
import youtube_dl
import asyncio

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(nextcord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=100):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = './music/' + data['title'] if stream else ytdl.prepare_filename(data)
        return filename

class MusicCog(commands.Cog):

	# Initialize cog into bot
	def __init__(self, bot):
		self.bot = bot
	
	# Command to join voice channel
	@commands.command(
		name="join",
		description="Command to connect to voice channel",
		usage=".join",
		aliases=['j']
	)
	async def join(self, ctx):
		channel = ctx.message.author.voice.channel
		await channel.connect()

	# Command to leave voice channel
	@commands.command(
		name="leave",
		description="Command to disconnect from channel",
		usage=".leave",
		aliases=['l']
	)
	async def leave(self, ctx):
		if(ctx.voice_client):
			await ctx.guild.voice_client.disconnect()
			await ctx.send("Bot left the voice channel")
		else:
			await ctx.send("Bot isn't in the voice channel")

	@commands.command(
		name="play",
		description="Play a song",
		usage=".play <URL>",
		aliases=['pl']
	)
	async def play(self,ctx,url):
		try:
			server = ctx.message.guild
			voice_channel = server.voice_client
			async with ctx.typing():
			    filename = await YTDLSource.from_url(url)
			    voice_channel.play(nextcord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
			await ctx.send('**Now playing:** {}'.format(filename))
		except:
			await ctx.send("The bot is not connected to a voice channel.")

	@commands.command(
		name='pause', 
		description='This command pauses the song',
		usage=".pause",
		aliases = ['.pz']
	)
	async def pause(self,ctx):
	    voice_client = ctx.message.guild.voice_client
	    if voice_client.is_playing():
	        await voice_client.pause()
	    else:
	        await ctx.send("The bot is not playing anything at the moment.")
	
	@commands.command(
		name='resume', 
		description='This command resumes the song',
		usage=".resume",
		aliases = ['.r']
	)
	async def resume(self,ctx):
	    voice_client = ctx.message.guild.voice_client
	    if voice_client.is_paused():
	        await voice_client.resume()
	    else:
	        await ctx.send("The bot was not playing anything before this. Use play_song command")

	@commands.command(
		name='stop', 
		description='This command stops the song',
		usage=".stop",
		aliases = ['.s']
	)
	async def stop(self,ctx):
	    voice_client = ctx.message.guild.voice_client
	    if voice_client.is_playing():
	        await voice_client.stop()
	    else:
	        await ctx.send("The bot is not playing anything at the moment.")

#ALWAYS KEEP THIS HERE
# This needs to be at the bottom of all cog files for the cog to be added to the main bot
def setup(bot):
	bot.add_cog(MusicCog(bot))