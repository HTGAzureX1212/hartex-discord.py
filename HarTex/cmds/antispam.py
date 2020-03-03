import discord
from discord.ext import commands

from core.classes import *

from datetime import datetime, timedelta

import yaml


def get_minimal_interval(guild_id):
    with open(f'configurations/{guild_id}_config.yaml', 'r') as accessor:
        reader = yaml.safe_load(accessor)

        interval = reader['plugins']['antispam']['settings']['interval']

    return interval


def get_ignored_channels(guild_id):
    with open(f'configurations/{guild_id}_config.yaml', 'r') as accessor:
        reader = yaml.safe_load(accessor)

    return reader['plugins']['antispam']['settings']['ignored_channels']


class Antispam(CategoryExtension):

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ctx = await self.bot.get_context(message)

        message_interval = get_minimal_interval(message.guild.id)

        message_channel: discord.TextChannel = message.channel

        ignored_channels = list(get_ignored_channels(message.guild.id))

        list_of_history = list(await message_channel.history().flatten())

        for msg in list_of_history[1:]:
            time_difference = message.created_at - msg.created_at

            if msg.author.bot:
                pass
            elif msg.author == message.author:
                for ID in ignored_channels:
                    if message_channel.id == ID:
                        pass
                    elif time_difference.total_seconds() < float(message_interval):
                        if ctx.valid:
                            pass

                            break
                        else:
                            await message.delete()
                            await message_channel.send("No spamming!")

                            break
                    else:
                        pass
            else:
                pass
        else:
            pass


def setup(hartex):
    hartex.add_cog(Antispam(hartex))
