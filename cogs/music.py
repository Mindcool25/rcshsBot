import nextcord
from nextcord.ext import commands
from nextcord.player import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from requests import get
from nextcord.utils import get

# ytdl_format_options = {
# 	'format' 				: 	'bestaudio/best',
# 	'outtmpl' 				:	'%(extractor)s-%(id)-%(title)s.%(ext)s',
# 	'restrictfilenames' 	:	True,
# 	'noplaylist'			:	True,
# 	'nocheckcertificate'	:	True,
# 	'ignoreerrors'			:	False,
# 	'logtostderr'			:	False,
# 	'quiet'					:	True,
# 	'no_warnings'			:	True,
# 	'default_search'		:	'auto',
# 	'source_address'		:	'0.0.0.0'
# }

# ffmpeg_options = {
# 	'options'	:	'-vn'
# }

# ytdl = YoutubeDL(ytdl_format_options)

# class YTDLSource(nextcord.PCMVolumeTransformer):
# 	def __init__(self, source, *, data, volume = 0.5):
# 		super().__init__(source, volume)

# 		self.data = data

# 		self.title 	=	data.get('title')
# 		self.url 	=	data.get('url')
	
# 	@classmethod
# 	async def from_url(cls, url, *, loop=None, stream=False):
# 		loop = loop or asyncio.get_event_loop()
# 		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

# 		if 'entries' in data:
# 			# take first item from a playlist
# 			data = data['entries'][0]

# 		filename = data['url'] if stream else ytdl.prepare_filename(data)
		
# 		return cls(nextcord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

def search(query):
	with YoutubeDL({'format' : 'bestaudio', 'noplaylist' : 'True'}) as ydl:
		try: get(query)
		except: info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
		else: info = ydl.extract_info(query, download=False)
	return (info, info['formats'][0]['url'])

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
		description="Play an audio",
		usage=".play <URL>",
		aliases=['.p']
	)
	async def play(ctx, *, query):
		FFMPEG_OPTS = {'before_options' : '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options' : '-vn'}

		video, source = search(query)
		voice = get(commands.voice_clients, guilf=ctx.guild)

		await ctx.send(f'Now playing {source}.')

		voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
		voice.is_playing()

#ALWAYS KEEP THIS HERE
# This needs to be at the bottom of all cog files for the cog to be added to the main bot
def setup(bot):
	bot.add_cog(MusicCog(bot))