import nextcord
from nextcord.ext import commands
import aiohttp
import random

def __aiter__(self):
        return self

async def __anext__(self):
    try:
        return next(self.iter)
    except StopIteration:
        raise StopAsyncIteration

class RedditCog(commands.Cog):
    # Initializing cog bot
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context    =   True,
        name            =   "memes",
        description     =   "Fetch memes from Hot",
        usage           =   ".memes",
        aliases         =   ['m']
    )
    async def memes(self, ctx):
        embed = nextcord.Embed(title="Ask, you shall receive", description="HAHA, meme go brr")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)


    @commands.command(
        pass_context    =   True,
        name            =   "prequel",
        description     =   "Fetches Prequel memes from Hot",
        usage           =   ".prequel",
        aliases         =   ['pre']
    )
    async def prequel(self, ctx):
        embed = nextcord.Embed(title="Ask, you shall receive", description="It will be done my lord")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/PrequelMemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @commands.command(
        pass_context    =   True,
        name            =   "wallpaper",
        description     =   "Fetch wallpapers from Hot",
        usage           =   ".wallpaper",
        aliases         =   ['wall']
    )
    async def wallpaper(self, ctx):
        embed = nextcord.Embed(title="Ask, you shall receive", description="epic")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/wallpaper/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @commands.command(
        pass_context    =   True,
        name            =   "wholesome",
        description     =   "Wholesome memes",
        usage           =   ".wholesome",
        aliases         =   ['w']
    )
    async def wholesome(self, ctx):
        embed = nextcord.Embed(title="Ask, you shall receive", description="how nice")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/wholesomememes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    # @commands.command(pass_context=True)
    # async def YOUR_CALL_COMMAND(ctx):
    #     embed = discord.Embed(title="EMBED_TITLE", description="EMBED_DESCRIPTION")
    #
    #     async with aiohttp.ClientSession() as cs:
    #         async with cs.get('SUBREDDIT_LINK/new.json?sort=hot') as r:
    #             res = await r.json()
    #             embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
    #             await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(RedditCog(bot))