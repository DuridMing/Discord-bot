'''
hackmd api combine discord bot.
@author:DuridMing
date: 03/23/2022
'''
# import discord
from discord import Embed
from discord.ext import commands

from core.classes import Cog_Extension
from config import *

import requests
import json

from time import time
from datetime import datetime

class note(Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
    
    @commands.command('id' ,brief="get note user info." ,description="$id ,get user info")
    async def _note_id(self ,ctx):        
        # get the user info 
        headers = {
            'Authorization': 'Bearer ' + HACKMD_TOKEN,
        }

        receive_data = requests.get('https://api.hackmd.io/v1/me' , headers=headers)
        print("[",datetime.now(), "] receive data from HackMD.")

        data = json.loads(receive_data.content)
        name = data['name']
        email = data['email']
        account = data['userPath']

        print("[",datetime.now(), "] HackMD account :",account)

        string = "name: "+ name+", "+ "email: "+ email+"."
        await ctx.send(string)

    @commands.command('find' ,brief="find note." ,description="$find <description> ,find the note.")
    async def _note_find(self, ctx , fi_str):
        # find note title 
        await ctx.send("processing...")
        headers = {
            'Authorization': 'Bearer ' + HACKMD_TOKEN,
        }

        st = time()
        recv = requests.get('https://api.hackmd.io/v1/notes' ,headers=headers)
        data = json.loads(recv.content)
        print("[",datetime.now(), "] receive data from HackMD.")
        
        # extract title from data
        title = []
        create_at = []
        for i in data:
            title.append(i['title'])
            timestamp = float(int(i['createdAt'])/1000)
            timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
            create_at.append(timestamp)

        # matching 
        match = []
        for num in range(len(title)):
            sl = title[num].lower()
            if fi_str.lower() in sl:
                match.append((title[num],create_at[num]))

        
        # result use embed
        embed=Embed(title="See what I find...", color=0x1de7d2 , timestamp=datetime.now(self.tz))
        embed.set_author(name="Durid_bot")
        embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")
        
        if len(match)>0:
            for res in match:
                embed.add_field(name=res[0], value="created at : "+res[1], inline=False)
        else :
            embed.add_field(name="Nothind find.", value="maybe you can change the description.")  

        end_time = time() - st 
        embed.set_footer(text=f"total used time: {round(end_time,1)} (s)")
        print("[", datetime.now(), "] ending find command,total used time: ",round(end_time, 1)," (s)")

        await ctx.send(embed=embed)

    @commands.command("create" ,brief="create note." ,description="$create <name>. create note.")
    async def _note_create(self,ctx,title):
        # create note
        #load basic content.
        jsfile = open("cmds/content.json", "r", encoding="utf-8")
        content = json.loads(jsfile.read())
        jsfile.close()
        content['basic']['title'] = str(title)
        content = json.dumps(content['basic'])

        headers = {
            'Authorization': 'Bearer ' + HACKMD_TOKEN,
            "Content-Type": "application/json"
        }
        recv = requests.post("https://api.hackmd.io/v1/notes", headers=headers , data=content)
        responce = json.loads(recv.content)
        print("[",datetime.now(), "] post new note to HackMD.")

        # resopnce 
        if recv.status_code == 201:
            embed = Embed(title="Successed",color=0x1de7d2, timestamp=datetime.now(self.tz))
            embed.set_author(name="Durid_bot")
            embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")
            embed.add_field(name="Note "+responce['title']+" Created", value="note id : "+str(responce['id']),inline=False)
            print("[",datetime.now(), "] Sueccessed.")
        else :
            # print(recv.status_code)
            embed = Embed(
                title="Oh No!", color=0x1de7d2, timestamp=datetime.now(self.tz))
            embed.set_author(name="Durid_bot")
            embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")
            embed.add_field(name="they have some troobule",
                            value="the web responce code: "+str(recv.status_code),inline=False)
            print("[",datetime.now(), "] Error with status code:",recv.status_code)

        # update content (bug cannot seting content and title at same time )
        # bug. update wii wrap all thing 
        '''
        payload = {
            "content": "---\n    image: https://i.imgur.com/XR6qAT2.jpg\n    robots: noindex,nofollow\n---\n\n \n\n<!-- this is CSS -->\n\n<style>\n\n.navbar-brand > span.hidden-xs {\n    color: transparent;\n}\n\n.navbar-brand > span.hidden-xs:before {\n    background-image: url(https://i.imgur.com/XR6qAT2.jpg);\n    background-repeat: no-repeat;\n    content: '　  　';\n    background-size: 60%;\n}\n\n.navbar-brand > span.hidden-xs:after {\n    margin-left: -3.8em;\n    content: 'HackMD';\n    color: #4b4645;\n}\n\n.navbar-brand > .fa-file-text {\n    display: none;\n}\n\n</style>"}
        payload = json.dumps(payload)

        pat = requests.patch("https://api.hackmd.io/v1/notes/"+str(responce['id']), headers=headers, data=payload)
        if pat.status_code == 202:
            embed.add_field(name="update note patch",value="successed")
        else :
            print(pat.content)
            embed.add_field(name="canot patch the note.", value="error code:"+str(pat.status_code))
        '''

        await ctx.send(embed=embed)
        await ctx.send(f"note id : {str(responce['id'])}")

    # they don't have methood to attach note.
    # update methood will wrap all thing.
    @commands.command("note", brief="comming soon...", description="comming soon...")
    async def _attach_note(self,ctx,note_id,*,content):
        await ctx.send("comming soon...")


def setup(bot):
    bot.add_cog(note(bot))