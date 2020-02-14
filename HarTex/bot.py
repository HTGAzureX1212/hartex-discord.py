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
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Activity(name="whatever link", type=discord.ActivityType.watching))
        print('Bot is ready.')

    async def on_guild_join(self, guild: discord.Guild):
        guild_id = guild.id

        with open('guilds.yaml', 'r+') as guild_add:
            content = yaml.safe_load(guild_add)

            content['connected_guilds'].append(guild_id)

            guild_add.seek(0)

            yaml.dump(content, guild_add)

            guild_add.truncate()

        with open(f'configurations/{guild_id}_config.yaml', 'w+') as guild_yaml_config_add:
            yaml.dump({'dashboard'.replace("'", ""): [guild.owner_id]}, guild_yaml_config_add, indent=4)

    async def on_guild_remove(self, guild: discord.Guild):
        guild_id = guild.id

        os.remove(f'configurations/{guild.id}_config.yaml')

        with open('guilds.yaml', 'r+') as guild_remove:
            content = yaml.safe_load(guild_remove)

            content['connected_guilds'].remove(guild_id)

            guild_remove.seek(0)

            yaml.dump(content, guild_remove)

            guild_remove.truncate()


hartex = HarTex()


@hartex.command()
async def load(ctx, extension):
    await ctx.load_extension(f'cmds/{extension}')
    await ctx.send(f"Successfully loaded extension: {extension}")


@hartex.command()
async def reload(ctx, extension):
    await ctx.reload_extension(f'cmds/{extension}')
    await ctx.send(f"Successfully reloaded extension: {extension}")


@hartex.command()
async def unload(ctx, extension):
    await ctx.unload_extension(f'cmds/{extension}')
    await ctx.send(f"Successfully unloaded extension: {extension}")


for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        hartex.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
    token = get_hartex_token()
    hartex.run(token)
