import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands

import yaml

import requests

from core.classes import *


def get_webhook(guild_id):
    with open(f'configurations/{guild_id}_config.yaml', 'r') as loader:
        accessor = yaml.safe_load(loader)

    return accessor['plugins']['utilities']['announce']


class Utilities(CategoryExtension):

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, channel: discord.TextChannel, message):
        get_webhook_stuff = get_webhook(guild_id=ctx.guild.id)

        webhook_token = str(get_webhook_stuff[channel.id]['webhook_token'])
        webhook_id = get_webhook_stuff[channel.id]['webhook_id']
        webhook_name = get_webhook_stuff[channel.id]['webhook_name']

        webhook = Webhook.partial(id=webhook_id, token=str(webhook_token), adapter=RequestsWebhookAdapter())

        webhook.send(message, username=str(webhook_name))


def setup(hartex):
    hartex.add_cog(Utilities(hartex))
