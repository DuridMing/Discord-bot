'''
finance modify commands.
using csv file to record data.
the file will be locate on ../finance/
'''
from pydoc import describe
import discord
from discord.ext import commands
from core.classes import Cog_Extension
from finance import finance
from datetime import datetime

class Money(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.group(invoke_without_command=True, brief="finance modify group command.", description="finance modify group command.")
    async def money(self,ctx):
        await ctx.send("the accounting commands.")
    
    @money.command(invoke_without_command=True , brief="pay",description="$money pay <dollars:int> <description>.")
    async def pay(self,ctx,dollars: int,*,describe):
        finance.writting(status="out" ,dollar=dollars ,describe=describe)
        await ctx.send("OK!")
    
    @money.command(invoke_without_command=True, brief="income", description="$money income <dollars:int> <description>.")
    async def income(self, ctx, dollars: int, *, describe):
        finance.writting(status="income", dollar=dollars, describe=describe)
        await ctx.send("OK!")
        
    def month_check(self, month):
        if month>12 or month <0 :
            raise commands.BadArgument("Month must be lower then 12 and upper then 0")

    @money.command(invoke_without_command=True, brief="total pay", description="$money totalpay <year:int> <month:int>.")
    async def totalpay(self, ctx ,year:int , month:int):
        self.month_check(month)
        result = finance.total(year,month)
        # print(result)
        
        if result < 0 :
            embed = discord.Embed(
                title="Error", color=0x1de7d2, timestamp=datetime.now(self.tz) ,description="Out of range.")
            embed.set_author(name="Durid_bot")
            embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")

        else:
            embed = discord.Embed(
                title=str(month)+"月 total pay", color=0x1de7d2, timestamp=datetime.now(self.tz))
            embed.set_author(name="Durid_bot")
            embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")
            embed.add_field(name="NTD $"+str(result) )
        
        await ctx.send(embed=embed)
        
        
    @commands.command(brief="finance chart.", description="$chart <month:int>finance chart for income and pay.")
    async def chart(self ,ctx ,month:int):
        self.month_check(month)
        pass


def setup(bot):
    bot.add_cog(Money(bot))