import discord
from discord.ext import commands

from core.classes import *


class Management(CategoryExtension):

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        await self.bot.close()


def setup(hartex):
    hartex.add_cog(Management(hartex))
