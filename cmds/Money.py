'''
finance modify commands.
using csv file to record data.
the file will be locate on ../finance/
'''
import discord
from discord import Embed ,File
from discord.ext import commands ,tasks
from datetime import date,datetime, timedelta
from dateutil.relativedelta import *
import pandas as pd
import os

from core.classes import Cog_Extension
from finance import finance

from config import *

class UnstableFile(Exception):
    pass

class Money(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
        self.tags = ['food', 'book', 'game','necessary','traffic', 'other']
        self.tags_string =  "'" + "','".join(map(str, self.tags)) + "'"
        self.until_next_month = False
        self.next_month=None
        self.monthly_report.start()
    
    def cog_unload(self):
        self.monthly_report.cancel()

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
            embed = Embed(
                title="Error", color=0x1de7d2, timestamp=datetime.now(self.tz) ,description="Out of range.")
            embed.set_author(name="Durid_bot")
            embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")
        else:
            embed = Embed(
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

        path =DATA_PATH+"figure/"
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
                picture = File(f)
                f.close()
                await ctx.send(file=picture)

    @money.command(invoke_without_command=True, brief="list this month descr.", description="$money lastlist")
    async def lastlist(self, ctx ):
        today = datetime.now(self.tz)
        month = today.strftime('%m')
        year = today.strftime('%Y')

        mdata = finance.list_all(year, month)
        if mdata is None :
            embed = Embed(
                title="Error", color=0x1de7d2, timestamp=datetime.now(self.tz) ,description="the csv data file not found.")
            embed.set_author(name="Durid_bot")
            embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")
        else:
            embed = Embed(
                title=str(month)+"月 pay list", color=0x1de7d2, timestamp=datetime.now(self.tz))
            embed.set_author(name="Durid_bot")
            embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")
            
            # locate data and create embed.
            for key, item in mdata:
                gpdata=mdata.get_group(key)
                mdescr=""
                for i in gpdata.index:
                    mdescr = mdescr + str("{} pay ${:<5d} for {}\n".format(gpdata.loc[i,"date"] , gpdata.loc[i,"dollar"],gpdata.loc[i,"describe"] ))
                embed.add_field(name=key, value=mdescr,inline=False)

        await ctx.send(embed=embed)

    
    @money.command(invoke_without_command=True, brief="list month descr.", description="$money paylist <year:int> <month:int>")
    async def paylist(self, ctx ,year:int ,month:int):
        if month <10 or month>0:
            month = "0"+str(month)
        
        mdata = finance.list_all(year, month)
        if mdata is None:
            embed = Embed(
                title="Error", color=0x1de7d2, timestamp=datetime.now(self.tz), description="the csv data file not found.")
            embed.set_author(name="Durid_bot")
            embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")
        else:
            embed = Embed(
                title=str(month)+"月 pay list", color=0x1de7d2, timestamp=datetime.now(self.tz))
            embed.set_author(name="Durid_bot")
            embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")

            # locate data and create embed.
            for key, item in mdata:
                gpdata = mdata.get_group(key)
                mdescr = ""
                for i in gpdata.index:
                    mdescr = mdescr + str("{} pay ${:<5d} for {}\n".format(
                        gpdata.loc[i, "date"], gpdata.loc[i, "dollar"], gpdata.loc[i, "describe"]))
                embed.add_field(name=key, value=mdescr, inline=False)

        await ctx.send(embed=embed)


    @commands.command(brief="finance copmpare chart.", description="$lcpr <past_year:int> <past_month:int>. compare to past two month.")
    async def lcpr(self ,ctx ,y2:int ,m2:int):
        self.month_check(m2)
        def mck(month):
            if month > 0 or month < 10:
                return "0"+str(month)
        m2 = mck(m2)

        # setting date to last month
        today = datetime.now(self.tz)
        first = today.replace(day=1)
        lastMonth = first - timedelta(days=1)
        y1 = lastMonth.strftime("%Y")
        m1 = lastMonth.strftime("%m")

        path = DATA_PATH+"figure/"
        pic_path = path+"finance-" + \
            "compare-"+str(y1)+"-"+str(m1)+"-and-" + \
            str(y2)+"-"+str(m2)+"-chart.jpg"

        try:
            if (m2 == datetime.now(self.tz).strftime("%m")):
                raise UnstableFile
            if not os.path.exists(pic_path):
                raise FileNotFoundError
            else:
                print("[", datetime.now(), "] find figure on :", pic_path)
        except FileNotFoundError:
            print("[", datetime.now(), "] figure not found.create new figure.")
            figure = finance.compare_chart(y1,m1,y2,m2)
        except UnstableFile:
            print("[", datetime.now(), "] figure compare with this month.")
            figure = finance.compare_chart(y1, m1, y2, m2)
        finally:
            print("[", datetime.now(), "] open figure :", pic_path)
            with open(pic_path, 'rb') as f:
                picture = File(f)
                f.close()
                await ctx.send(file=picture)


    @commands.command(brief="finance copmpare chart.", description="$tcpr <year1:int> <month1:int> <year2:int> <month2:int>. compare two month. cannot use on this month.")
    async def tcpr(self ,ctx ,y1:int ,m1:int ,y2:int ,m2:int):
        self.month_check(m1)
        self.month_check(m2)
        tmonth = datetime.now(self.tz).strftime("%m")

        if m1 < m2:
            def swap( a, b ):
                return b, a
            swap(m1,m2)
            swap(y1,y2)

        def mck(month):
            if month > 0 or month < 10:
                return "0"+str(month)
        m1 = mck(m1)
        m2 = mck(m2)

        path = DATA_PATH+"figure/"
        pic_path = path+"finance-" + \
            "compare-"+str(y1)+"-"+str(m1)+"-and-" + \
            str(y2)+"-"+str(m2)+"-chart.jpg"

        try:
            if (m1 == tmonth) or (m2 == tmonth):
                raise UnstableFile
            if not os.path.exists(pic_path):
                raise FileNotFoundError
            else:
                print("[", datetime.now(), "] find figure on :", pic_path)
        except FileNotFoundError:
            print("[", datetime.now(), "] figure not found.create new figure.")
            figure = finance.compare_chart(y1,m1,y2,m2)
        except UnstableFile:
            print("[", datetime.now(), "] figure compare with this month.")
            figure = finance.compare_chart(y1, m1, y2, m2)
        finally:
            print("[", datetime.now(), "] open figure :", pic_path)
            with open(pic_path, 'rb') as f:
                picture = File(f)
                f.close()
                await ctx.send(file=picture)

    # tasking loop for one month
    # create a new csv file and send a new compare figure
    @tasks.loop(seconds=10)
    async def monthly_report(self):
        channel = self.bot.get_channel(MONTH_REPORT_CHANNEL)
        
        if not self.until_next_month:
            today = datetime.now(self.tz)
            delta = today.replace(day=1)
            delta = delta + relativedelta(months=+1)
            self.next_month = delta.strftime('%Y-%m-%d')
            print("[", datetime.now(), "] set next report date on ",self.next_month)
            self.until_next_month = True
        today = datetime.now(self.tz).strftime('%Y-%m-%d')
        if today == self.next_month:
            finance.create_csv()

            # setting date to last month
            td = datetime.now(self.tz)
            first = td.replace(day=1)
            lastMonth = first - timedelta(days=1)
            y1 = lastMonth.strftime("%Y")
            m1 = lastMonth.strftime("%m")

            path = DATA_PATH+"figure/"
            pic_path = path+"finance-" + str(y1)+"-"+str(m1)+"-chart.jpg"
            figure = finance.monthly_chart(y1,m1)
  
            with open(pic_path, 'rb') as f:
                picture = File(f)
                f.close()
                await channel.send(file=picture)

            self.until_next_month = False

    


def setup(bot):
    bot.add_cog(Money(bot))
