import discord
from discord import Embed
from discord import Guild
from discord.ext import commands

from core.classes import *


class Info(CategoryExtension):

    @commands.command()
    async def botinfo(self, ctx):

        infoEmbed = Embed(title="HarTex Info", description="My Information", colour=0xa6f7ff)
        infoEmbed.add_field(name="Owner", value="HTGAzureX1212#2450", inline=True)
        infoEmbed.add_field(name="Created at", value="2 Jan 2020, 09.25 [UCT +0]", inline=True)
        infoEmbed.add_field(name="Current server prefix", value=".", inline=False)
        infoEmbed.add_field(name="Command count", value="4", inline=False)
        infoEmbed.add_field(name="Language versions", value="Python 3.8.1\ndiscord.py 1.2.5")

        await ctx.send("", embed=infoEmbed)

    @commands.command()
    async def guildinfo(self, ctx):

        # The guild the command is ran in
        guild: Guild = ctx.guild

        # The no. of channels of the guild.
        channelCount = len(list(guild.channels))

        # The no. of text channels of the guild.
        textChannelCount = len(list(guild.text_channels))

        # The no. of voice channels of the guild.
        voiceChannelCount = len(list(guild.voice_channels))

        guildInfo = Embed(colour=0xa6f7ff)
        guildInfo.title = "Information of {}".format(guild.name)
        guildInfo.description = "What is {}?".format(guild.name)
        guildInfo.add_field(name="Guild Name", value="{}".format(guild.name), inline=False)
        guildInfo.add_field(name="Guild Owner", value=guild.owner, inline=False)
        guildInfo.add_field(name="Members", value=str(guild.member_count), inline=False)
        guildInfo.add_field(name="Channels", value=str(channelCount), inline=False)
        guildInfo.add_field(name="Text Channels", value=str(textChannelCount), inline=False)
        guildInfo.add_field(name="Voice Channels", value=str(voiceChannelCount), inline=False)
        guildInfo.add_field(name="Voice Region", value=guild.region, inline=False)

        await ctx.send("", embed=guildInfo)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member):

        memberRoles = list(role for role in member.roles)

        em = Embed(colour=0xa6f7ff)
        em.title = "Information of {}".format(member)
        em.description = "Who is {}?".format(member)

        em.set_thumbnail(url=member.avatar_url)

        em.add_field(name="Username and Discriminator", value=str(member), inline=False)

        em.add_field(name="Status", value=member.status, inline=False)

        em.add_field(name="Joined At:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        em.add_field(name="Roles: {}".format(len(memberRoles)), value="{}".join(role.mention for role in memberRoles).replace("{}", "\n"))

        em.add_field(name="Top Role", value=member.top_role)

        await ctx.send("", embed=em)


def setup(hartex):
    hartex.add_cog(Info(hartex))
