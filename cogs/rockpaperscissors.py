import nextcord
from nextcord.ext import commands
import random

class rps(commands.Cog):
    @commands.command(
		name="rps",
		description="Play Rock Paper Scissors",
		usage=".rps <option (r, p, s)>",
		aliases=['rockpaperscissors']
	)
	async def rps_command(self, ctx, *, option):
		"""Play Rock Paper Scissors"""
		if message == "s":
			options = ['I Chose Rock! You Lose!', 'I Chose Scissors. We Tied.', 'I Chose Paper... I Lost...']
			await ctx.send(f'{random.choice(options)}')
			return
		elif message == 'p':
			options = ['I Chose Scissors! You Lose!', 'I Chose Paper. We Tied.', 'I Chose Rock... I Lost...']
			await ctx.send(f'{random.choice(options)}')
			return
		elif message == "r":
			options = ['I Chose Paper! You Lose!', 'I Chose Rock. Wes Tied.', 'I Chose Scissors... I Lost...']
			await ctx.send(f'{random.choice(options)}')
			return
		else:
			await ctx.send(f'Uhh... What? That Is Not An Option')

def setup(bot):
	bot.add_cog(Basic(bot))
