import discord
from discord import Colour
from discord import Embed
from discord.ext import commands

from core.classes import *

import disputils


class Help(CategoryExtension):

    @commands.command()
    async def help(self, ctx):

        helpEmbed = Embed(title="HarTex Help", description="Common Moderation Commands", colour=0xa6f7ff)
        helpEmbed.add_field(name="kick", value="Kicks a user.", inline=False)
        helpEmbed.add_field(name="ban", value="Bans a user.", inline=False)
        helpEmbed.add_field(name="unban", value="Unbans a user.", inline=False)
        helpEmbed.add_field(name="mute", value="Mutes a user.", inline=False)
        helpEmbed.add_field(name="unmute", value="Unmutes a user.", inline=False)
        helpEmbed.add_field(name="tempmute", value="Temporarily mutes a user.", inline=False)

        await ctx.send("", embed=helpEmbed)


def setup(hartex):
    hartex.add_cog(Help(hartex))
    
