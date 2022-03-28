'''
discord bot for local use.
author: @Durid_Ming
'''
import discord
from discord.ext import commands
import os
from datetime import datetime

from config import *
from Help import Help

if __name__ =="__main__":

    bot = commands.Bot(command_prefix='$' , help_command=Help())

    @bot.command()
    @commands.is_owner()
    async def load(ctx, extension):
        bot.load_extension(f"cmds.{extension}")
        embed = discord.Embed(
            title='Load', description=f'{extension} successfully loaded', color=0xff00c8)
        await ctx.send(embed=embed)

    @bot.command()
    @commands.is_owner()
    async def unload(ctx, extension):
        bot.unload_extension(f"cmds.{extension}")
        embed = discord.Embed(
            title='unload', description=f'{extension} successfully unloaded', color=0xff00c8)
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
        print("[",datetime.now(),"] the bot is on ready.")
    
    @bot.event
    async def on_command_error(ctx ,error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Unknown command. Use $help to get some help")
            
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing argument. use $help <command> to get more info.")
            # await ctx.send(error)

        if isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument. use $help <command> to get more info.")
            # await ctx.send(error)

    # bot.get_cog(Greetings(bot))
    for filename in os.listdir("./cmds"):
        if filename.endswith('.py'):
            bot.load_extension(f"cmds.{filename[:-3]}")
    # Token 
    bot.run(DISORD_BOT_TOKEN) 

