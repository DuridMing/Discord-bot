from discord.ext import commands
from core.classes import Cog_Extension

class mcds(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)

    # testing command
    # @commands.command(name="test", brief='test', description='test')
    # async def _test(self,ctx ,status ,dollar ,describe):
    #     writting(status=status ,dollar=dollar ,describe=describe)
    #     await ctx.send("OK")

    @commands.command(name="ping", brief="return bot lantecy.", description="$ping ,return lantecy")
    async def _ping(self,ctx):
        await ctx.send(f'{round(self.bot.latency*1000)}(ms)')


        

def setup(bot):
    bot.add_cog(mcds(bot))