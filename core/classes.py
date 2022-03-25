import discord
from discord.ext import commands
from datetime import datetime ,timezone ,timedelta
from config import *


class Cog_Extension(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.tz = timezone(timedelta(hours=+TIMEZONE))

