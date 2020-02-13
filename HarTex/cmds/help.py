import discord
from discord import Colour
from discord import Embed
from discord.ext import commands

from core.classes import *
from core.configvalues import *


class Help(CategoryExtension):

    @commands.command()
    async def help(self, ctx, command=None):
        """
        .help

        A custom help command.
        """
        if command is None:
            helpEmbed = Embed(title="HarTex Help", description="Common Moderation Commands", footer="Execute `help <command>` to get more information about one command.", colour=0xa6f7ff)
            helpEmbed.add_field(name="kick", value="Kicks a user.", inline=False)
            helpEmbed.add_field(name="ban", value="Bans a user.", inline=False)
            helpEmbed.add_field(name="unban", value="Unbans a user.", inline=False)
            helpEmbed.add_field(name="mute", value="Mutes a user.", inline=False)
            helpEmbed.add_field(name="unmute", value="Unmutes a user.", inline=False)
            helpEmbed.add_field(name="tempmute", value="Temporarily mutes a user.", inline=False)

            await ctx.send(embed=helpEmbed)
        elif command == "kick":
            helpKickEmbed = Embed(title="HarTex Help: Kick", description="Kick: Usage", colour=0xa6f7ff)
            helpKickEmbed.add_field(name="Usage", value="kick <member: **discord.Member**> <reason: **optional**>", inline=False)
            helpKickEmbed.add_field(name="Description", value="Kicks a member.", inline=False)

            await ctx.send(embed=helpKickEmbed)
        elif command == "ban":
            helpBanEmbed = Embed(title="HarTex Help: Ban", description="Ban: Usage", colour=0xa6f7ff)
            helpBanEmbed.add_field(name="Usage", value="ban <member: **discord.Member**> <reason: **optional**>", inline=False)
            helpBanEmbed.add_field(name="Description", value="Bans a member.", inline=False)

            await ctx.send(embed=helpBanEmbed)
        elif command == "unban":
            helpUnbanEmbed = Embed(title="HarTex Help: Unban", description="Unban: Usage", colour=0xa6f7ff)
            helpUnbanEmbed.add_field(name="Usage", value="unban <member: **discord.Member**> <reason: **optional**>", inline=False)
            helpUnbanEmbed.add_field(name="Description", value="Unbans a member.", inline=False)

            await ctx.send(embed=helpUnbanEmbed)
        elif command == "mute":
            helpMuteEmbed = Embed(title="HarTex Help: Mute", description="Mute: Usage", colour=0xa6f7ff)
            helpMuteEmbed.add_field(name="Usage", value="mute <member: **discord.Member**> <reason: **optional**>", inline=False)
            helpMuteEmbed.add_field(name="Description", value="Mutes a member.", inline=False)

            await ctx.send(embed=helpMuteEmbed)
        elif command == "unmute":
            helpUnmuteEmbed = Embed(title="HarTex Help: Unmute", description="Unmute: Usage", colour=0xa6f7ff)
            helpUnmuteEmbed.add_field(name="Usage", value="unmute <member: **discord.Member**> <reason: **optional**>", inline=False)
            helpUnmuteEmbed.add_field(name="Description", value="Unmutes a member.", inline=False)

            await ctx.send(embed=helpUnmuteEmbed)
        elif command == "tempmute":
            helpTempmuteEmbed = Embed(title="HarTex Help: Tempmute", description="Tempmute: Usage", colour=0xa6f7ff)
            helpTempmuteEmbed.add_field(name="Usage", value="unban <member: **discord.Member**> <reason: **optional**>", inline=False)
            helpTempmuteEmbed.add_field(name="Description", value="Unbans a member.", inline=False)

            await ctx.send(embed=helpTempmuteEmbed)


def setup(hartex):
    hartex.add_cog(Help(hartex))
