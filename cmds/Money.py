'''
finance modify commands.
using csv file to record data.
the file will be locate on ../finance/
'''
from re import L
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os

from core.classes import Cog_Extension
from finance import finance

class Money(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
        self.tags = ['food', 'book', 'game','necessary','traffic', 'other']
        self.tags_string =  "'" + "','".join(map(str, self.tags)) + "'"

    @commands.group(invoke_without_command=True, brief="finance modify group command.", description="finance modify group command.")
    async def money(self,ctx):
        await ctx.send("the accounting commands.")
    
    def tag_check(self,tg):
        tg = tg.lower()
        if tg == "nes":
            tg = "necessary"
        for t in self.tags:
            if tg == t:
                return tg
        raise commands.BadArgument(
                "Tag error.tag must be "+self.tags_string)


    @money.command(invoke_without_command=True , brief="pay",description="$money pay <tag:str> <dollars:int> <description>.")
    async def pay(self, ctx, tag: str, dollars: int, *, describe):
        tag = self.tag_check(tag)        
        finance.writting(status="pay" ,tag=tag,dollar=dollars ,describe=describe)
        await ctx.send("OK!")
    
    @money.command(invoke_without_command=True, brief="income", description="$money income <dollars:int> <description>.")
    async def income(self, ctx, tag: str,dollars: int, *, describe):
        finance.writting(status="income", tag="income",dollar=dollars, describe=describe)
        await ctx.send("OK!")
        
    def month_check(self, month):
        if month>12 or month <0 :
            raise commands.BadArgument("Month must be lower then 12 and upper then 0")

    @money.command(invoke_without_command=True, brief="total pay", description="$money tpay <year:int> <month:int>.")
    async def tpay(self, ctx ,year:int , month:int):
        self.month_check(month)
        result = finance.total(year,month)
        
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
            embed.add_field(name="NTD $"+str(result),value="\u200b")

        await ctx.send(embed=embed)
        
    @money.command(invoke_without_command=True, brief="last month chart", description="$money last.")
    async def last(self, ctx):

        # setting date to last month
        today = datetime.now(self.tz)
        first = today.replace(day=1)
        lastMonth = first - timedelta(days=1)
        year = lastMonth.strftime("%Y")
        month = lastMonth.strftime("%m")

        path = "finance/figure/"
        pic_path = path+"finance-" + str(year)+"-"+str(month)+"-chart.jpg"

        try:
            if not os.path.exists(pic_path):
                raise FileNotFoundError
            else :
                print("[",datetime.now(),"] find figure on :",pic_path)
        except FileNotFoundError:
            print("[",datetime.now(), "] figure not found.create new figure.")
            figure = finance.lastest_chart()
        finally:
            print("[", datetime.now(), "] open figure :",pic_path)
            with open(pic_path, 'rb') as f:
                picture = discord.File(f)
                f.close()
                await ctx.send(file=picture)

        
    @commands.command(brief="finance copmpare chart.", description="$lcompare <past_year:int> <past_month:int>. compare to latest.")
    async def lcompare(self ,ctx ,year:int ,month:int):
        self.month_check(month)
        pass

    @commands.command(brief="finance copmpare chart.", description="$tcompare <year1:int> <month1:int> <year2:int> <month2:int>. compare two month.")
    async def tcompare(self ,ctx ,year1:int ,month1:int ,yeat2:int ,month2:int):
        pass

def setup(bot):
    bot.add_cog(Money(bot))