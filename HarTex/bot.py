import discord
from discord.ext import commands

from core.classes import *

import yaml

import os

__author = "Harry."

__version = "1.7.0"


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
        await self.change_presence(status=discord.Status.online, activity=discord.Activity(name="Harry.#2450 developing", type=discord.ActivityType.watching))
        print('Bot is ready.')

    async def on_guild_join(self, guild: discord.Guild):
        guild_id = guild.id

        with open('guilds.yaml', 'r') as guild_add:
            content = yaml.safe_load(guild_add)

            for guildID in content['whitelisted_guilds']:
                if guild_id == int(guildID):

                    with open(f'configurations/{guild_id}_config.yaml', 'a+') as guild_yaml_config_add:
                        yaml.dump({'dashboard'.replace("'", ""): {guild.owner_id: 'admin'.replace("'", "")}}, guild_yaml_config_add, indent=2)

                    with open(f'infractions/{guild_id}_infractions.yaml', 'a+') as guild_infractions_add:
                        yaml.dump({'infractions'.replace("'", "")}, guild_infractions_add, indent=2)

                    with open(f'levels/{guild_id}_levels.yaml', 'a+') as guild_levels_add:
                        yaml.dump({'levels'.replace("'", "")}, guild_levels_add, indent=2)
                else:
                    await guild.leave()

    async def on_guild_remove(self, guild: discord.Guild):
        guild_id = guild.id

        os.remove(f'configurations/{guild_id}_config.yaml')

        os.remove(f'infractions/{guild_id}_infractions.yaml')

        os.remove(f'infractions/{guild_id}_infractions.yaml')

        with open('guilds.yaml', 'r+') as guild_remove:
            content = yaml.safe_load(guild_remove)

            content['connected_guilds'].remove(guild_id)

            guild_remove.seek(0)

            yaml.dump(content, guild_remove)

            guild_remove.truncate()


hartex = HarTex()


@hartex.command()
async def load(ctx, extension):
    await ctx.load_extension(f'cmds.{extension}')
    await ctx.send(f"Successfully loaded extension: {extension}")


@hartex.command()
async def reload(ctx, extension):
    await ctx.reload_extension(f'cmds.{extension}')
    await ctx.send(f"Successfully reloaded extension: {extension}")


@hartex.command()
async def unload(ctx, extension):
    await ctx.unload_extension(f'cmds.{extension}')
    await ctx.send(f"Successfully unloaded extension: {extension}")


for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        hartex.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
    token = get_hartex_token()
    hartex.run(token)
