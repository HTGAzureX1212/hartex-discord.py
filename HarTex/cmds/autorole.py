import discord
from discord.ext import commands
from discord.utils import get

import yaml

from core.classes import *


def get_role_to_give_on_join(guild_id):
    with open(f'configurations/{guild_id}_config.yaml', 'r') as loader:
        accessor = yaml.safe_load(loader)

        role = accessor['plugins']['autorole']['role']

    return role


class Autorole(CategoryExtension):

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        role_to_give = get(member.guild.roles, id=get_role_to_give_on_join(guild_id=member.guild.id))

        await member.add_roles(role_to_give)


def setup(hartex):
    hartex.add_cog(Autorole(hartex))
