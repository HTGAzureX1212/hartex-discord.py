import discord
from discord.ext import commands

from discord.utils import get

from core.classes import *

from asyncio import sleep

import yaml


class Moderation(CategoryExtension):

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *reasontext):
        """
        .kick <member: discord.Member> <reasontext(optional)>

        Kicks a member.
        """
        guild_to_load_config: discord.Guild = member.guild

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        def get_channel_id():
            with open(f'configurations/{guild_to_load_config.id}_config.yaml', 'r') as channel_to_get:
                mod_log_channel = yaml.safe_load(channel_to_get)

                channel_id: discord.TextChannel = guild_to_load_config.get_channel(
                    mod_log_channel['plugins']['logging']['type']['moderation_log']['channel'])

            return channel_id

        # Kicks the member.
        await member.kick(reason=reasonoutput)

        # Sends a confirmation message.
        await ctx.send(f"Successfully kicked {member} for {reasonoutput}.")

        channelID = get_channel_id()

        kickEmbed = discord.Embed(title=":foot: A Member has been Kicked from the server", colour=0xa6f7ff)

        kickEmbed.add_field(name="Member", value=f"{member.mention}", inline=False)

        kickEmbed.add_field(name="Reason", value=f"{reasonoutput}")

        await channelID.send(embed=kickEmbed)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *reasontext):
        """
        .ban <member: discord.Member> <reasontext(optional)>

        Bans a member.
        """

        guild_to_load_config = member.guild

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        def get_channel_id():
            with open(f'configurations/{guild_to_load_config.id}_config.yaml', 'r') as channel_to_get:
                mod_log_channel = yaml.safe_load(channel_to_get)

                channel_id: discord.TextChannel = guild_to_load_config.get_channel(mod_log_channel['plugins']['logging']['type']['moderation_log']['channel'])

            return channel_id

        channelID = get_channel_id()

        kickEmbed = discord.Embed(title=":hammer: A Member has been Banned from the server", colour=0xa6f7ff)

        kickEmbed.add_field(name="Member", value=f"{member.mention}", inline=False)

        kickEmbed.add_field(name="Reason", value=f"{reasonoutput}")

        await channelID.send(embed=kickEmbed)

        # Bans the member.
        await member.ban(reason=reasonoutput)

        # Sends a confirmation message.
        await ctx.send(f"Successfully banned {member} for {reasonoutput}.")

    @commands.command()
    async def unban(self, ctx, member: discord.Member, *reasontext):
        """
        .unban <member: discord.Member> <reasontext(optional)>

        Unbans a member.
        """

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        guild_to_load_config = member.guild

        def get_channel_id():
            with open(f'configurations/{guild_to_load_config.id}_config.yaml', 'r') as channel_to_get:
                mod_log_channel = yaml.safe_load(channel_to_get)

                channel_id: discord.TextChannel = guild_to_load_config.get_channel(mod_log_channel['plugins']['logging']['type']['moderation_log']['channel'])

            return channel_id

        channelID = get_channel_id()

        kickEmbed = discord.Embed(title=":hammer: A Member has been Unbanned from the server", colour=0xa6f7ff)

        kickEmbed.add_field(name="Member", value=f"{member.mention}", inline=False)

        kickEmbed.add_field(name="Reason", value=f"{reasonoutput}")

        await channelID.send(embed=kickEmbed)

        # Unbans the member.
        await member.unban(reason=reasonoutput)

        # Sends a confirmation message.
        await ctx.send(f"Successfully unbanned {member} for {reasonoutput}.")

    @commands.command()
    async def mute(self, ctx, member: discord.Member, *reasontext):
        """
        .mute <member: discord.Member> <reasontext(optional)>

        Mutes a member.
        """

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        guild_to_load_config = member.guild

        def get_channel_id():
            with open(f'configurations/{guild_to_load_config.id}_config.yaml', 'r') as channel_to_get:
                mod_log_channel = yaml.safe_load(channel_to_get)

                channel_id: discord.TextChannel = guild_to_load_config.get_channel(
                    mod_log_channel['plugins']['logging']['type']['moderation_log']['channel'])

            return channel_id

        channelID = get_channel_id()

        kickEmbed = discord.Embed(title=":no_mouth: A Member has been Muted from the server", colour=0xa6f7ff)

        kickEmbed.add_field(name="Member", value=f"{member.mention}", inline=False)

        kickEmbed.add_field(name="Reason", value=f"{reasonoutput}")

        await channelID.send(embed=kickEmbed)

        # Looks for the Muted role in the corresponding guild.
        mutedRole = get(ctx.guild.roles, name="Muted")

        # Adds the role to the mentioned member.
        await member.add_roles(mutedRole)

        # Sends a confirmation message.
        await ctx.send(f"Successfully muted {member} for {reasonoutput}.")

    @commands.command()
    async def unmute(self, ctx, member: discord.Member, *reasontext):
        """
        .unmute <member: discord.Member> <reasontext(optional)>

        Unmutes a member.
        """

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        guild_to_load_config = member.guild

        def get_channel_id():
            with open(f'configurations/{guild_to_load_config.id}_config.yaml', 'r') as channel_to_get:
                mod_log_channel = yaml.safe_load(channel_to_get)

                channel_id: discord.TextChannel = guild_to_load_config.get_channel(
                    mod_log_channel['plugins']['logging']['type']['moderation_log']['channel'])

            return channel_id

        channelID = get_channel_id()

        kickEmbed = discord.Embed(title=":open_mouth: A Member has been Unmuted from the server", colour=0xa6f7ff)

        kickEmbed.add_field(name="Member", value=f"{member.mention}", inline=False)

        kickEmbed.add_field(name="Reason", value=f"{reasonoutput}")

        await channelID.send(embed=kickEmbed)

        # Looks for the Muted role in the corresponding guild.
        mutedRole = get(ctx.guild.roles, name="Muted")

        # Removes the role to the mentioned member.
        await member.remove_roles(mutedRole)

        # Sends a confirmation message.
        await ctx.send(f"Successfully unmuted {member} for {reasonoutput}.")

    @commands.command()
    async def tempmute(self, ctx, member: discord.Member, time: str,  *reasontext):
        """
        .tempmute <member: discord.Member> <time> <reasontext(optional)>

        Temporarily mutes a member.
        """

        sleepDuration = 0

        for _ in time:
            if 'd' in _ or 'D' in _:
                sleepDuration += 24 * 60 * 60 * (int(time.replace('d', ' ').replace('D', ' ')))
            if 'h' in _ or 'H' in _:
                sleepDuration += 60 * 60 * (int(time.replace('h', ' ').replace('H', ' ')))
            if 'm' in _ or 'M' in _:
                sleepDuration += 60 * (int(time.replace('m', ' ').replace('M', ' ')))
            if 's' in _ or 'S' in _:
                sleepDuration += (int(time.replace('s', ' ').replace('S', ' ')))

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        guild_to_load_config = member.guild

        def get_channel_id():
            with open(f'configurations/{guild_to_load_config.id}_config.yaml', 'r') as channel_to_get:
                mod_log_channel = yaml.safe_load(channel_to_get)

                channel_id: discord.TextChannel = guild_to_load_config.get_channel(
                    mod_log_channel['plugins']['logging']['type']['moderation_log']['channel'])

            return channel_id

        channelID = get_channel_id()

        kickEmbed = discord.Embed(title=":no_mouth: A Member has been Temp-muted from the server", colour=0xa6f7ff)

        kickEmbed.add_field(name="Member", value=f"{member.mention}", inline=False)

        kickEmbed.add_field(name="Reason", value=f"{reasonoutput}")

        await channelID.send(embed=kickEmbed)

        # Looks for the Muted role in the corresponding guild.
        mutedRole = get(ctx.guild.roles, name="Muted")

        # Confirmation message.
        await ctx.send(f"Successfully muted {member} for {sleepDuration}s for {reasonoutput}.")

        # Adds the Muted role.
        await member.add_roles(mutedRole)

        # Sleeps for the sleepDuration.
        await sleep(sleepDuration)

        # Removes the role to the mentioned member.
        await member.remove_roles(mutedRole)

        # Sends another confirmation message for unmuted.
        await ctx.send("{} has been unmuted.".format(member))

        unkickEmbed = discord.Embed(title=":open_mouth: A Member has been Unmuted from the server", colour=0xa6f7ff)

        unkickEmbed.add_field(name="Member", value=f"{member.mention}", inline=False)

        await channelID.send(embed=kickEmbed)

    @commands.command()
    async def ceasech(self, ctx, channel: discord.TextChannel):
        """
        .ceasech <channel: discord.TextChannel>

        Ceases a channel.
        """

        # Changes the permission of the mentioned channel.
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)

        # Sends a confirmation message.
        await ctx.send(f"{channel} has been ceased.")

    @commands.command()
    async def unceasech(self, ctx, channel: discord.TextChannel):
        """
        .unceasech <channel: discord.TextChannel>

        Unceases a channel.
        """

        # Changes the permission of the mentioned channel.
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)

        # Sends a confirmation message.
        await ctx.send(f"{channel} has been unceased.")

    @commands.command()
    async def ceasegd(self, ctx):
        """
        .ceasegd

        Ceases the guild.
        """

        permissionOverride = discord.Permissions()
        permissionOverride.send_messages = False

        role: discord.Role = get(ctx.guild.roles, name="Member")

        await role.edit(permissions=permissionOverride)
        await ctx.send("Successfully ceased guild.")

    @commands.command()
    async def unceasegd(self, ctx):
        """
        .unceasegd

        Unceases the guild.
        """

        permissionOverride = discord.Permissions()
        permissionOverride.send_messages = True

        role: discord.Role = get(ctx.guild.roles, name="Member")

        await role.edit(permissions=permissionOverride)
        await ctx.send("Successfully unceased guild.")

    @commands.command()
    async def warn(self, ctx, member: discord.Member, *reasontext):
        warned_member_guild = member.guild

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        with open(f'infractions/{warned_member_guild.id}_infractions.yaml', 'r+') as infraction_add:
            accessor = yaml.safe_load(infraction_add)

            infractions = accessor['infractions'][member.id]

        accessor['infractions'][member.id] += 1

        infractions += 1

        with open(f'infractions/{warned_member_guild.id}_infractions.yaml', 'r+') as infraction_add:
            yaml.dump(accessor, infraction_add)

        await ctx.send(f"Successfully warned {member} for {reasonoutput}, total warnings: {infractions}")

    @commands.command()
    async def pardon(self, ctx, member: discord.Member, *reasontext):
        warned_member_guild = member.guild

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        with open(f'infractions/{warned_member_guild.id}_infractions.yaml', 'r+') as infraction_add:
            accessor = yaml.safe_load(infraction_add)

            infractions = accessor['infractions'][member.id]

        accessor['infractions'][member.id] -= 1

        infractions -= 1

        with open(f'infractions/{warned_member_guild.id}_infractions.yaml', 'r+') as infraction_add:
            yaml.dump(accessor, infraction_add)

        await ctx.send(f"Successfully pardoned {member} for {reasonoutput}, total warnings: {infractions}")


def setup(hartex):
    hartex.add_cog(Moderation(hartex))
