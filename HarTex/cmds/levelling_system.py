import discord
from discord.ext import commands

from core.classes import *

import yaml

import random

from datetime import datetime, timedelta


class LevellingSystem(CategoryExtension):
    def __init__(self, bot):
        super().__init__(bot)
        self._cd = commands.CooldownMapping.from_cooldown(1.0, 60.0, commands.BucketType.user)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        time = message.created_at
        messages = []

        async for msg in message.channel.history(oldest_first=False):
            if msg.author == message.author and msg.created_at != time:
                messages.append(msg)

        last_msg_time: datetime = messages[1].created_at

        delta = time - last_msg_time

        message_guild: discord.Guild = message.guild

        user_id = message.author.id

        xp_to_add = random.randint(15, 25)

        with open(f'levels/{message_guild.id}_levels.yaml', 'r') as level_access:
            accessor = yaml.safe_load(level_access)

            level_dict = dict(accessor)

        if delta.seconds < 30:
            pass
        else:
            if message.author.bot:
                pass
            else:
                if level_dict is None:
                    level_dict[user_id]['level'] = 0
                    level_dict[user_id]['xp'] = xp_to_add

                    with open(f'levels/{message.guild.id}_levels.yaml', 'a+') as add_user:
                        yaml.dump(level_dict, add_user, indent=2)
                elif user_id not in level_dict:
                    try:
                        level_dict[user_id]['level'] = 0
                        level_dict[user_id]['xp'] = xp_to_add

                        with open(f'levels/{message_guild.id}_levels.yaml', 'a+') as add_user:
                            yaml.dump(level_dict, add_user, indent=2)
                    except KeyError:
                        with open(f'levels/{message_guild.id}_levels.yaml', 'a+') as add_user_when_key_error:
                            yaml.dump({user_id: {'level': 0, 'xp': xp_to_add}}, add_user_when_key_error, indent=2)
                else:
                    level_dict[user_id]['xp'] += xp_to_add

                    if int(level_dict[user_id]['xp']) >= 5 * (int(level_dict[user_id]['level']) ** 2) + 50 * int(level_dict[user_id]['level']) + 100:
                        level_dict[user_id]['level'] += 1
                        level_dict[user_id]['xp'] = int(level_dict[user_id]['xp']) - (5 * (int(level_dict[user_id]['level'] - 1) ** 2) + 50 * int(level_dict[user_id]['level'] - 1) + 100)

                        level = level_dict[user_id]['level']

                        with open(f'levels/{message.guild.id}_levels.yaml', 'w') as add_level:
                            yaml.dump(level_dict, add_level, indent=2)

                        await message.channel.send(f'Congratulations, {message.author.mention}, you are now **__Level {level}__**!')
                    else:
                        with open(f'levels/{message.guild.id}_levels.yaml', 'w') as add_xp:
                            yaml.dump(level_dict, add_xp, indent=2)

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):

        rank_card = discord.Embed(colour=0xa6f7ff)

        if member is None:
            try:
                user_guild: discord.Guild = ctx.message.guild

                user: discord.User = ctx.message.author

                with open(f'levels/{user_guild.id}_levels.yaml') as accessor:
                    data = yaml.safe_load(accessor)

                    dict(data)

                levels = []

                for m_id in [m.id for m in ctx.message.guild.members]:
                    try:
                        level = data[m_id]['level']
                        xp = data[m_id]['xp']

                        levels.append((m_id, float(str(data[m_id]['level']) + '.' + str(data[m_id]['xp']))))
                    except KeyError:
                        continue

                levels.sort(key=lambda tuple_item: tuple_item[1], reverse=True)

                current_xp = data[user.id]['xp']

                level_end_xp = 5 * (int(data[user.id]['level']) ** 2) + 50 * int(data[user.id]['level']) + 100

                rank_position = levels.index((user.id, float(str(data[user.id]['level']) + '.' + str(data[user.id]['xp'])))) + 1

                rank_card.title = f"{user.display_name}'s Rank Card"
                rank_card.add_field(name="Rank", value=f"#{rank_position}", inline=False)
                rank_card.add_field(name="Level", value=f"{str(data[user.id]['level'])}")
                rank_card.add_field(name="Experience", value=f"{current_xp} / {level_end_xp} XP")

                await ctx.send(embed=rank_card)
            except KeyError:
                await ctx.send("Please send some messages!")
        else:
            if not member.bot:
                member_guild: discord.Guild = member.guild

                try:
                    with open(f'levels/{member_guild.id}_levels.yaml') as accessor:
                        data = yaml.safe_load(accessor)

                    print(data)

                    levels = []

                    for m_id in [m.id for m in ctx.message.guild.members]:
                        try:
                            level = data[m_id]['level']
                            xp = data[m_id]['xp']

                            levels.append((m_id, float(str(level) + '.' + str(xp))))
                        except KeyError:
                            continue

                    levels.sort(key=lambda x: x[1], reverse=True)

                    current_xp = data[member.id]['xp']

                    level_end_xp = 5 * (int(data[member.id]['level']) ** 2) + 50 * int(data[member.id]['level']) + 100

                    rank_position = levels.index((member.id, float(str(data[member.id]['level']) + '.' + str(data[member.id]['xp'])))) + 1

                    rank_card.title = f"{member.display_name}'s Rank Card"
                    rank_card.add_field(name="Rank", value=f"#{rank_position}", inline=False)
                    rank_card.add_field(name="Level", value=f"{str(data[member.id]['level'])}")
                    rank_card.add_field(name="Experience", value=f"{current_xp} / {level_end_xp} XP")

                    await ctx.send(embed=rank_card)
                except KeyError:
                    await ctx.send("The user you specified doesn't have a rank card!")
            else:
                await ctx.send("Bots can't have a rank card!")

    @commands.command()
    async def levels(self, ctx):
        with open(f'levels/{ctx.message.guild.id}_levels.yaml', 'r') as leaderboard:
            data = yaml.safe_load(leaderboard)

        levels = []

        for m_id in [m.id for m in ctx.message.guild.members]:
            try:
                level = data[m_id]['level']
                xp = data[m_id]['xp']

                levels.append((m_id, float(str(level) + "." + str(xp))))
            except KeyError:
                continue

        levels.sort(key=lambda x: x[1], reverse=True)

        lb_embed = discord.Embed(title=f"Levelling Leaderboard for {ctx.message.guild.name}", colour=0xa6f7ff)

        for stat in levels:
            member = ctx.message.guild.get_member(stat[0])

            rank = levels.index((member.id, float(str(data[member.id]['level']) + "." + str(data[member.id]['xp'])))) + 1

            lb_embed.add_field(name=f"Rank {rank} - {member}", value=f"Level {data[member.id]['level']} | {data[member.id]['xp']} / {(5 * (int(data[member.id]['level']) ** 2) + 50 * int(data[member.id]['level']) + 100)} XP", inline=False)

        await ctx.send(embed=lb_embed)


def setup(hartex):
    hartex.add_cog(LevellingSystem(hartex))
