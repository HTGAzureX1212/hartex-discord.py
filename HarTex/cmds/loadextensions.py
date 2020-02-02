import discord
from discord.ext import commands

from core.classes import *


class LoadExtensions(CategoryExtension):
    @commands.command()
    async def load(self, ctx, extension):
        ctx.load_extension(f'cmds.{extension}')

    @commands.command()
    async def reload(self, ctx, extension):
        ctx.reload_extension(f'cmds.{extension}')

    @commands.command()
    async def unload(self, ctx, extension):
        ctx.unload_extension(f'cmds.{extension}')


def setup(hartex):
    hartex.add_cog(LoadExtensions(hartex))
