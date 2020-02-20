import discord
from discord import Embed
from discord import Guild
from discord.ext import commands

from core.classes import *


class Info(CategoryExtension):

    @commands.command()
    async def botinfo(self, ctx):
        """
        .botinfo

        Information of the bot.
        """

        infoEmbed = Embed(title="HarTex Info", description="My Information", colour=0xa6f7ff)
        infoEmbed.add_field(name="Owner", value="HTGAzureX1212#2450", inline=True)
        infoEmbed.add_field(name="Created at", value="2 Jan 2020, 09.25 [UCT +0]", inline=True)
        infoEmbed.add_field(name="Current server prefix", value=".", inline=False)
        infoEmbed.add_field(name="Command count", value="17", inline=False)
        infoEmbed.add_field(name="Language versions", value="Python 3.8.1\ndiscord.py 1.3.1")

        await ctx.send("", embed=infoEmbed)

    @commands.command()
    async def guildinfo(self, ctx):
        current_guild: discord.Guild = ctx.guild

        member_counts = {
            "bot count": 0,
            "human count": 0
        }
        member_statuses = {
            "online": 0,
            "idle": 0,
            "dnd": 0,
            "offline/invisible": 0
        }
        safety_settings = {
            "2FA Setting": current_guild.mfa_level,
            "verification level": current_guild.verification_level
        }

        # Calculation of the number of bot and human users in a guild.
        for member in current_guild.members:
            if member.bot:
                member_counts["bot count"] += 1
            else:
                member_counts["human count"] += 1

        # Calculation of the number of members in different statuses in a guild.
        for member in current_guild.members:
            if str(member.status) == "online":
                member_statuses["online"] += 1
            elif str(member.status) == "idle":
                member_statuses["idle"] += 1
            elif str(member.status) == "dnd":
                member_statuses["dnd"] += 1
            elif str(member.status) == "offline":
                member_statuses["offline/invisible"] += 1

        # Verification levels

        if safety_settings['verification level'] == discord.VerificationLevel.none:
            safety_settings['verification level'] = "Not set"
        elif safety_settings['verification level'] == discord.VerificationLevel.low:
            safety_settings['verification level'] = "Low"
        elif safety_settings['verification level'] == discord.VerificationLevel.medium:
            safety_settings['verification level'] = "Moderate"
        elif safety_settings['verification level'] == discord.VerificationLevel.high or safety_settings['verification level'] == discord.VerificationLevel.table_flip:
            safety_settings['verification level'] = "High"
        elif safety_settings['verification level'] == discord.VerificationLevel.extreme or safety_settings['verification level'] == discord.VerificationLevel.double_table_flip:
            safety_settings['verification level'] = "Extreme"

        # Boolean - 2FA enabled
        if safety_settings['2FA Setting'] == 1:
            safety_settings['2FA Setting'] = "True"
        elif safety_settings['2FA Setting'] == 0:
            safety_settings['2FA Setting'] = "False"

        # Embed
        guild_info = discord.Embed(title=f"Information of {current_guild.name}", colour=0xa6f7ff)
        guild_info.add_field(name="Server ID", value=f"{current_guild.id}", inline=False)
        guild_info.add_field(name="Server Owner, Owner ID", value=f"{current_guild.owner}, {current_guild.owner_id}", inline=False)
        guild_info.add_field(name="Number of Categories", value=f"{len(current_guild.categories)}", inline=False)
        guild_info.add_field(name="Number of Text Channels", value=f"{len(current_guild.text_channels)}", inline=False)
        guild_info.add_field(name="Number of Voice Channels", value=f"{len(current_guild.voice_channels)}", inline=False)
        guild_info.add_field(name="Members", value=f"Total Number of Members: {current_guild.member_count}\nHuman Members: {member_counts['human count']}\nBot Members: {member_counts['bot count']}\nStatus - Online: {member_statuses['online']}\nStatus - Idle: {member_statuses['idle']}\nStatus - Do Not Disturb: {member_statuses['dnd']}\nStatus - Offline: {member_statuses['offline/invisible']}", inline=False)
        guild_info.add_field(name="2FA Enabled?", value=f"{safety_settings['2FA Setting']}", inline=False)
        guild_info.add_field(name="Verification Level", value=f"{safety_settings['verification level']}", inline=False)
        guild_info.add_field(name="Voice Region", value=f"{current_guild.region}", inline=False)
        guild_info.add_field(name="Server Created At", value=f"{current_guild.created_at}", inline=False)
        guild_info.set_thumbnail(url=current_guild.icon_url)

        await ctx.send(embed=guild_info)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member):
        """
        .userinfo <member: discord.Member>

        Information of the user.
        """

        memberRoles = list(role for role in member.roles)

        em = Embed(title=f"Information of {member}", description=f"Who is {member}?", colour=0xa6f7ff)
        em.description = "Who is {}?".format(member)

        em.set_thumbnail(url=member.avatar_url)

        em.add_field(name="Username and Discriminator", value=str(member), inline=False)

        em.add_field(name="Status", value=member.status, inline=False)

        em.add_field(name="Joined At:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        em.add_field(name="Roles: {}".format(len(memberRoles)), value="{}".join(role.mention for role in memberRoles).replace("{}", "\n"))

        em.add_field(name="Top Role", value=member.top_role.mention)

        await ctx.send("", embed=em)


def setup(hartex):
    hartex.add_cog(Info(hartex))
