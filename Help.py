import discord
from discord.ext import commands

from datetime import datetime ,timezone ,timedelta

class Help(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
        self.tz = timezone(timedelta(hours=+8))
    
    # for $help
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
                title="Commands", 
                color=0x1de7d2, 
                description="the command perfix is '$'.\n use $help <command> to get more info.",
                timestamp=datetime.now(self.tz))
        embed.set_author(name="Durid_bot")
        embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")
        
        for cog in mapping :
            cds = []
            cds_str = ""
            cds_des = ""
            if cog is not None:
                # cds = [command.name, command.brief for command in mapping[cog]]
                for command in mapping[cog]:
                    if command.brief is None:
                        command.brief = "no desription."
                    cds.append((command.name , command.brief))
                # print(cds)
                for c in cds:
                    cds_str = cds_str +""+c[0]+"\n"
                    cds_des = cds_des +""+c[1]+"\n"
                
                embed.add_field(name= cog.qualified_name , value = cds_str,inline=True)
                embed.add_field(name="description"  , value=cds_des ,inline=True)
                embed.add_field(name="\u200b", value="\u200b", inline=True)

        await self.get_destination().send(embed=embed)

    # for $help <cog>
    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=cog.qualified_name+" Commands",
            color=0x1de7d2,
            description="use $help <command> to get more info.",
            timestamp=datetime.now(self.tz))
        embed.set_author(name="Durid_bot")
        embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")

        for command in cog.get_commands():
            if command is not None:
                embed.add_field(name="$"+command.name , value = command.description,inline=False)
        
        await self.get_destination().send(embed=embed)

    # for $help <command>
    async def send_command_help(self, command):
        embed = discord.Embed(
            title="$"+command.name,
            color=0x1de7d2,
            timestamp=datetime.now(self.tz))
        embed.set_author(name="Durid_bot")
        embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")

        embed.add_field(name="How to use?" , value=command.description)

        await self.get_destination().send(embed=embed)
    
    # for $help <group>
    async def send_group_help(self, group):
        embed = discord.Embed(
            title=group.name+" Commands",
            color=0x1de7d2,
            timestamp=datetime.now(self.tz))
        embed.set_author(name="Durid_bot")
        embed.set_thumbnail(url="https://i.imgur.com/XR6qAT2.jpg")

        for index ,command in enumerate(group.commands):
            embed.add_field(name="$"+group.name+" "+command.name ,value=command.description , inline=False)

        await self.get_destination().send(embed=embed)
