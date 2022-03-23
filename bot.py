'''
discord bot for local use.
author: @Durid_Ming
'''
from config import *
import discord
from discord.ext import commands
import os

if __name__ =="__main__":

    bot = commands.Bot(command_prefix='$')

    @bot.command()
    @commands.is_owner()
    async def load(ctx, extension):
        bot.load_extension(f"cmds.{extension}")
        embed = discord.Embed(
            title='Load', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.send(embed=embed)

    @bot.command()
    @commands.is_owner()
    async def unload(ctx, extension):
        bot.unload_extension(f"cmds.{extension}")
        embed = discord.Embed(
            title='unload', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.send(embed=embed)
    

    @bot.command()
    @commands.is_owner()
    async def reload(ctx, extension):
        bot.reload_extension(f"cmds.{extension}")
        embed = discord.Embed(
            title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.send(embed=embed)

    @bot.event
    async def on_ready():
        print("login user:",bot.user)

    # bot.get_cog(Greetings(bot))
    for filename in os.listdir("./cmds"):
        if filename.endswith('.py'):
            bot.load_extension(f"cmds.{filename[:-3]}")
    # Token 
    bot.run(DISORD_BOT_TOKEN) 

