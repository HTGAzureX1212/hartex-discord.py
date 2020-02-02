import discord
from discord.ext import commands

from core.classes import *

import yaml

import os


def get_hartex_token():
    with open('token.yaml', 'r') as tokenAccessor:
        yamlReader = yaml.safe_load(tokenAccessor)

        tokenValue = yamlReader['bot']['token']

        return tokenValue


def get_hartex_prefix():
    with open('config.yaml', 'r') as prefixAccessor:
        yamlReader = yaml.safe_load(prefixAccessor)

        prefix = yamlReader['bot_interface']['command_prefix']

        return prefix


def get_hartex_nickname():
    with open('config.yaml', 'r') as nicknameAccessor:
        yamlReader = yaml.safe_load(nicknameAccessor)

        nickname = yamlReader['bot_interface']['guild_nickname']

        return nickname


hartexPrefix = get_hartex_prefix()

hartexNickname = get_hartex_nickname()


class HarTex(commands.Bot):  # this is a modified discord.commands.Bot class
    def __init__(self):
        super(HarTex, self).__init__(command_prefix=hartexPrefix, help_command=None)

    async def on_ready(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Activity(name="whatever link", type=discord.ActivityType.watching))
        print('Bot is ready.')

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.CommandNotFound):
            errorI = discord.Embed(title="**Command Error**",
                                   description="This command raised an exception. Read below for more information.",
                                   colour=0xa6f7ff)
            errorI.add_field(name="Exception Code", value="HTe001", inline=False)
            errorI.add_field(name="Exception Description", value="Command not found.", inline=False)

            await ctx.send("", embed=errorI)

        if isinstance(exception, commands.MissingRequiredArgument):
            errorII = discord.Embed(title="**Command Error**",
                                    description="This command raised an exception. Read below for more information.",
                                    colour=0xa6f7ff)
            errorII.add_field(name="Exception Code", value="HTe002", inline=False)
            errorII.add_field(name="Exception Description", value='A required argument is missing. Execute `.help <command>` to view the required arguments.')

            await ctx.send("", embed=errorII)

        if isinstance(exception, commands.DisabledCommand):
            errorIII = discord.Embed(title="**Command Error**",
                                     description="This command raised an exception. Read below for information.",
                                     colour=0xa6f7ff)
            errorIII.add_field(name="Exception Code", value="HTe003", inline=False)
            errorIII.add_field(name="Exception Description", value="This command is disabled. Please enable it in the YAML configuration.")

            await ctx.send("", embed=errorIII)


hartex = HarTex()


for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        hartex.load_extension(f'cmds.{filename[:-3]}')


if __name__ == "__main__":
    token = get_hartex_token()
    hartex.run(token)
    
