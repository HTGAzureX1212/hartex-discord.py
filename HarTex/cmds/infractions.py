import discord
from discord.ext import commands

from core.classes import *

import yaml

infractions_of_a_member = None


def get_guild_infractions(guild_id):
    with open(f'infractions/{guild_id}_infractions.yaml', 'r') as inf:
        accessor = yaml.safe_load(inf)

    return accessor


class Infractions(CategoryExtension):

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def infractions(self, ctx, search=None, member: discord.Member = None):
        global infractions_of_a_member

        if search is None:
            raise commands.MissingRequiredArgument
        elif member is None:
            await ctx.send("Please specify a member to view infractions!")
        else:
            get_infractions = get_guild_infractions(member.guild.id)

            try:
                infractions_of_a_member = get_infractions['infractions'][member.id]
            except KeyError:
                infractions_of_a_member = 0

            if infractions_of_a_member is None or infractions_of_a_member == 0:
                await ctx.send("The user has no infractions.")
            else:
                await ctx.send(f"The user has {infractions_of_a_member} infraction(s).")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def infraction(self, ctx, remove=None, member: discord.Member = None, number_of_infractions=None):
        global infractions_of_a_member

        if remove is None:
            raise commands.MissingRequiredArgument
        elif member is None:
            await ctx.send("Please specify a member to remove infraction(s)!")
        elif number_of_infractions is None:
            await ctx.send("Please specify the number of infraction(s) to remove!")
        else:
            get_infractions = get_guild_infractions(member.guild.id)

            try:
                infractions_of_a_member = get_infractions['infractions'][member.id]
            except KeyError:
                raise KeyError

            get_infractions['infractions'][member.id] -= int(number_of_infractions)

            with open(f'infractions/{member.guild.id}_infractions.yaml', 'r+') as infraction_add:
                yaml.dump(get_infractions, infraction_add)


def setup(hartex):
    hartex.add_cog(Infractions(hartex))
