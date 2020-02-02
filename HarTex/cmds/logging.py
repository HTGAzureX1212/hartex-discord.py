import discord
from discord.ext import commands

from core.classes import *

from core.configvalues import *


class Logging(CategoryExtension):
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        MemberLogChannel = LoggingChannel.MemberLoggingChannel

        JoinEmbed = discord.Embed(title=":inbox_tray: Member Joined", colour=0xa6f7ff)
        JoinEmbed.add_field(name="Member", value=f"@{member}")
        JoinEmbed.set_thumbnail(url=member.avatar_url)

        await MemberLogChannel.send("", embed=JoinEmbed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        MemberLogChannel = LoggingChannel.MemberLoggingChannel

        LeaveEmbed = discord.Embed(title=":outbox_tray: Member Left", colour=0xa6f7ff)
        LeaveEmbed.add_field(name="Member", value=f"@{member}")
        LeaveEmbed.set_thumbnail(url=member.avatar_url)

        await MemberLogChannel.send("", embed=LeaveEmbed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        MessageLogChannel: discord.TextChannel = commands.Bot.get_channel(id=LoggingChannel.MessageLoggingChannel)

        EditEmbed = discord.Embed(title=":pencil: Message Edited", colour=0xa6f7ff)
        EditEmbed.add_field(name="Message Edited By", value=before.author.mention, inline=False)
        EditEmbed.add_field(name="Message Channel", value=before.channel, inline=False)
        EditEmbed.add_field(name="Before", value=before.content, inline=True)
        EditEmbed.add_field(name='After', value=after.content, inline=True)

        await MessageLogChannel.send("", embed=EditEmbed)


def setup(hartex):
    hartex.add_cog(Logging(hartex))
    
