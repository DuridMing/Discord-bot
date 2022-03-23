from discord.ext import commands
from core.classes import Cog_Extension

class mcds(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(name="test")
    async def _test(self,ctx, arg):
        await ctx.send(arg)

    @commands.command(name="ping")
    async def _ping(self,ctx):
        await ctx.send(f'{round(self.bot.latency*1000)}(ms)')

        

def setup(bot):
    bot.add_cog(mcds(bot))