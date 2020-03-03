import discord
from discord.ext import commands

from core.classes import *


class Administrator(CategoryExtension):

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def role(self, ctx, action=None, role: discord.Role = None, member: discord.Member = None):
        try:
            if action is None:
                await ctx.send("Please specify an action: `add` or `remove`.")
            elif role is None:
                await ctx.send("Please specify a role by typing its name or mentioning it.")
            elif member is None:
                await ctx.send("Please specify a member by mentioning him/her.")
            else:
                if action == "add":
                    await member.add_roles(role)
                    await ctx.send(f"Gave {member} the {role} role!")
                elif action == "remove":
                    await member.remove_roles(role)
                    await ctx.send(f"Removed the {role} role from {member}!")
        except Exception as e:
            await ctx.send(f"This command raised an exception: \n```{e}```")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def list(self, ctx, item_to_list=None):
        if item_to_list is None:
            await ctx.send("Please specify a category to list: \nRoles: `roles`")
        elif item_to_list == "roles":
            guild_to_list_roles: discord.Guild = ctx.guild

            guild_roles = guild_to_list_roles.roles

            roles_looped = 0

            roles = discord.Embed(title=f"Roles of {guild_to_list_roles}", colour=0xa6f7ff)

            await ctx.send("Fetching roles...")

            for role in guild_roles:
                roles_looped += 1

                roles.add_field(name=f"Role {roles_looped}", value=f"{role.name}", inline=False)
            else:
                await ctx.send("Here is the list of roles:")

            await ctx.send(embed=roles)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def slowmode(self, ctx, enable_or_disable=None, channel: discord.TextChannel = None, duration=None):
        if enable_or_disable is None:
            await ctx.send("You need to specify whether to enable or disable the slowmode!")
        elif enable_or_disable == "enable":
            if duration is None:
                await ctx.send("Please specify the interval duration of the slowmode!")

            await channel.edit(slowmode_delay=duration)
            await ctx.send(f"Enabled slowmode of {duration} seconds for <#{channel.id}>.")
        elif enable_or_disable == "disable":
            if duration is None:
                pass

            await ctx.send(f"Disabled slowmode for <#{channel.id}>.")
            await channel.edit(slowmode_delay=0)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def roleinfo(self, ctx, role: discord.Role = None):
        role_info = discord.Embed(title=f"Information About Role: {role.name}")
        role_info.add_field(name="Role Name", value=role.name, inline=False)
        role_info.add_field(name="Role ID", value=role.id, inline=False)
        role_info.add_field(name="Role Colour", value=role.colour, inline=False)
        role_info.add_field(name="Role Created At", value=role.created_at, inline=False)
        role_info.add_field(name="Number of Members That Have This Role", value=str(len(role.members)))

        await ctx.send(embed=role_info)

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, change_or_remove=None, member: discord.Member = None, new_nickname=None):
        if change_or_remove is None:
            await ctx.send("Please specify adding or removing a nickname!")
        elif member is None:
            await ctx.send("Please specify a member to change his/her nickname!")
        elif change_or_remove == "change":
            if new_nickname is None:
                await ctx.send(f"Please specify a nickname!")
            else:
                await member.edit(nick=new_nickname)
                await ctx.send(f"Nickname changed for {member}.")
        elif change_or_remove == "remove":
            await member.edit(nick=None)
            await ctx.send(f"Nickname removed from {member}.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def invites(self, ctx):
        guild: discord.Guild = ctx.guild

        list_of_invites = list(await guild.invites())

        invites_embed = discord.Embed(title=f"{guild.name}'s Invites", colour=0xa6f7ff)

        for invite in list_of_invites:
            invites_embed.add_field(name="Invite Code", value=invite.code, inline=False)
        else:
            await ctx.send(embed=invites_embed)


def setup(hartex):
    hartex.add_cog(Administrator(hartex))
