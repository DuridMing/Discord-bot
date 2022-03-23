'''
hackmd api combine discord bot.
@author:DuridMing
date: 03/23/2022
'''
from discord.ext import commands

from core.classes import Cog_Extension
from config import *

import requests
import json


class note(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
    
    @commands.command('id')
    async def _note_id(self ,cxt):        
        headers = {
            'Authorization': 'Bearer ' + HACKMD_TOKEN,
        }

        receive_data = requests.get('https://api.hackmd.io/v1/me' , headers=headers)
        data = json.loads(receive_data.content)
        name = data['name']
        email = data['email']
        account = data['userPath']

        print(name , email , account)

        string = "name: "+ name+", "+ "email: "+ email+"."
        await cxt.send(string)

    @commands.command('list')
    async def _note_list(self, cxt):
        headers = {
            'Authorization': 'Bearer ' + HACKMD_TOKEN,
        }
        recv = requests.get('https://api.hackmd.io/v1/notes' ,headers=headers)


def setup(bot):
    bot.add_cog(note(bot))