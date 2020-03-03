import discord
from discord.ext import commands

from core.classes import *


class WhitelistApplications(CategoryExtension):

    @commands.command()
    @commands.is_owner()
    async def accept(self, ctx, user: discord.User):
        await user.create_dm()

        await user.send(content="**__Thanks for reaching out to HarTex!__**\n\nWe have received your whitelist application form.\n\nWe consider many aspects when accepting or denying a whitelist application:\n- Is the server has more than 250 members;\n- Does the server encourage NSFW content;\n- etc.\n\n\n I wonder what your result would be!\n\nYou have been accepted.\nYou can invite the bot via this link:\nhttps://discordapp.com/oauth2/authorize?client_id=667684156385394711&permissions=8&scope=bot")

    @commands.command()
    @commands.is_owner()
    async def deny(self, ctx, user: discord.User):
        await user.create_dm()

        await user.send(
            content="**__Thanks for reaching out to HarTex!__**\n\nWe have received your whitelist application form.\n\nWe consider many aspects when accepting or denying a whitelist application:\n- Is the server has more than 250 members;\n- Does the server encourage NSFW content;\n- etc.\n\n\n I wonder what your result would be!\n\nYou have been denied.\nYour server either doesn't have more than 250 members, but you are welcome to apply again after 30 days.\nAnything before that is automatically ignored.")


def setup(hartex):
    hartex.add_cog(WhitelistApplications(hartex))
