import discord
from discord.ext import commands

from discord.utils import get

from core.configvalues import *

from core.classes import *

from asyncio import sleep


class Moderation(CategoryExtension):

    ownerRole: discord.Role = OwnerRole.ownerRoleID

    adminRole: discord.Role = AdministratorRole.adminRoleID

    modRole: discord.Role = ModeratorRole.moderRoleID

    isKickEnabled = CommandsEnabledOrDisabled.KickCommandEnabled

    @commands.command(enabled=False)
    @commands.has_role(modRole)
    async def kick(self, ctx, member: discord.Member, *reasontext):

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        # Kicks the member.
        await member.kick(reason=reasonoutput)

        # Sends a confirmation message.
        await ctx.send(f"Successfully kicked {member} for {reasonoutput}.")

    @commands.command()
    @commands.has_role(modRole)
    async def ban(self, ctx, member: discord.Member, *reasontext):

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        # Bans the member.
        await member.ban(reason=reasonoutput)

        # Sends a confirmation message.
        await ctx.send(f"Successfully banned {member} for {reasonoutput}.")

    @commands.command()
    @commands.has_role(modRole)
    async def unban(self, ctx, member: discord.Member, *reasontext):

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        # Unbans the member.
        await member.unban(reason=reasonoutput)

        # Sends a confirmation message.
        await ctx.send(f"Successfully banned {member} for {reasonoutput}.")

    @commands.command()
    @commands.has_role(modRole)
    async def mute(self, ctx, member: discord.Member, *reasontext):

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        # Looks for the Muted role in the corresponding guild.
        mutedRole = get(ctx.guild.roles, name="Muted")

        # Adds the role to the mentioned member.
        await member.add_roles(mutedRole)

        # Sends a confirmation message.
        await ctx.send(f"Successfully muted {member} for {reasonoutput}.")

    @commands.command()
    @commands.has_role(modRole)
    async def unmute(self, ctx, member: discord.Member, *reasontext):

        reasonoutput = ""

        for word in reasontext:
            reasonoutput += word
            reasonoutput += " "
            reasonoutput.strip()

        # Looks for the Muted role in the corresponding guild.
        mutedRole = get(ctx.guild.roles, name="Muted")

        # Removes the role to the mentioned member.
        await member.remove_roles(mutedRole)

        # Sends a confirmation message.
        await ctx.send(f"Successfully unmuted {member} for {reasonoutput}.")

    @commands.command()
    @commands.has_role(modRole)
    async def tempmute(self, ctx, member: discord.Member, time: str,  *reasontext):

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

    @commands.command()
    @commands.has_role(adminRole)
    async def ceasech(self, ctx, channel: discord.TextChannel):

        # Changes the permission of the mentioned channel.
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)

        # Sends a confirmation message.
        await ctx.send(f"{channel} has been ceased.")

    @commands.command()
    @commands.has_role(adminRole)
    async def unceasech(self, ctx, channel: discord.TextChannel):

        # Changes the permission of the mentioned channel.
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)

        # Sends a confirmation message.
        await ctx.send(f"{channel} has been unceased.")

    @commands.command()
    @commands.has_role(adminRole)
    async def ceasegd(self, ctx):

        permissionOverride = discord.Permissions()
        permissionOverride.send_messages = False

        role: discord.Role = get(ctx.guild.roles, name="Member")

        await role.edit(permissions=permissionOverride)
        await ctx.send("Successfully ceased guild.")

    @commands.command()
    @commands.has_role(adminRole)
    async def unceasegd(self, ctx):

        permissionOverride = discord.Permissions()
        permissionOverride.send_messages = True

        role: discord.Role = get(ctx.guild.roles, name="Member")

        await role.edit(permissions=permissionOverride)
        await ctx.send("Successfully unceased guild.")


def setup(hartex):
    hartex.add_cog(Moderation(hartex))
