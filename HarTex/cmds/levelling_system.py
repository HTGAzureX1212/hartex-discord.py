import discord
from discord.ext import commands

from core.classes import *

import yaml

import random

import asyncio

from PIL import Image, ImageDraw, ImageFont

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

        print(delta.seconds)

        if delta.seconds < 30:
            pass
        else:
            if message.author.bot:
                pass
            else:
                if level_dict is None:
                    level_dict[user_id]['level'] = 0
                    level_dict[user_id]['xp'] = 0

                    with open(f'levels/{message.guild.id}_levels.yaml', 'a+') as add_user:
                        yaml.dump(level_dict, add_user, indent=2)
                elif user_id not in level_dict:
                    try:
                        level_dict[user_id]['level'] = 0
                        level_dict[user_id]['xp'] = 0

                        with open(f'levels/{message_guild.id}_levels.yaml', 'a+') as add_user:
                            yaml.dump(level_dict, add_user, indent=2)
                    except KeyError:
                        with open(f'levels/{message_guild.id}_levels.yaml', 'a+') as add_user_when_key_error:
                            yaml.dump({user_id: {'level': [0], 'xp': [0]}}, add_user_when_key_error, indent=2)
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
        x = 100
        y = 200
        w = 700
        h = 50

        rank_card = Image.new('RGB', (934, 282), color=0xafb6b8)

        rank_card_font = ImageFont.truetype('Font/01_APompadourTextSample.ttf', 50)

        rank_card_font2 = ImageFont.truetype('Font/02_APompadourTextSample.ttf', 100)

        rank_card_font3 = ImageFont.truetype('Font/03_APompadourTextSample.ttf', 40)

        draw_rank_card = ImageDraw.Draw(rank_card)

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

                levels.sort(key=lambda x: x[1], reverse=True)

                current_xp = data[user.id]['xp']

                level_end_xp = 5 * (int(data[user.id]['level']) ** 2) + 50 * int(data[user.id]['level']) + 100

                rank_position = levels.index((user.id, float(str(data[user.id]['level']) + '.' + str(data[user.id]['xp'])))) + 1

                draw_rank_card.text((450, 50), "Rank", fill="white", font=rank_card_font)
                draw_rank_card.text((575, 14), f"{rank_position}", fill="white", font=rank_card_font2)
                draw_rank_card.text((675, 50), "Level", fill=0x006eff, font=rank_card_font)
                draw_rank_card.text((810, 14), str(data[user.id]['level']), fill=0x006eff, font=rank_card_font2)
                draw_rank_card.text((50, 125), f"{user.name}", fill="white", font=rank_card_font)
                draw_rank_card.text((650, 140), f"{current_xp}", fill="white", font=rank_card_font3)
                draw_rank_card.text((750, 140), f" / {level_end_xp} XP", fill=0x333434, font=rank_card_font3)

                # Progress Bar Background
                draw_rank_card.ellipse((x + w, y, x + h + w, y + h), fill="white")
                draw_rank_card.ellipse((x, y, x + h, y + h), fill="white")
                draw_rank_card.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill="white")

                # Count
                progress = float(current_xp / level_end_xp)

                if progress <= 0:
                    progress = 0.01
                elif progress > 1:
                    progress = 1

                w *= progress

                draw_rank_card.ellipse((x + w, y, x + h + w, y + h), fill=0x006eff)
                draw_rank_card.ellipse((x, y, x + h, y + h), fill=0x006eff)
                draw_rank_card.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=0x006eff)

                rank_card.save('card.png')

                await ctx.send(file=discord.File('card.png'))
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

                    draw_rank_card.text((450, 50), "Rank", fill="white", font=rank_card_font)
                    draw_rank_card.text((575, 14), f"{rank_position}", fill="white", font=rank_card_font2)
                    draw_rank_card.text((675, 50), "Level", fill=0x006eff, font=rank_card_font)
                    draw_rank_card.text((810, 14), str(data[member.id]['level']), fill=0x006eff, font=rank_card_font2)
                    draw_rank_card.text((50, 125), f"{member.display_name}", fill="white",
                                        font=rank_card_font)
                    draw_rank_card.text((650, 140), f"{current_xp}", fill="white", font=rank_card_font3)
                    draw_rank_card.text((750, 140), f" / {level_end_xp} XP", fill=0x333434, font=rank_card_font3)

                    # Progress Bar Background
                    draw_rank_card.ellipse((x + w, y, x + h + w, y + h), fill="white")
                    draw_rank_card.ellipse((x, y, x + h, y + h), fill="white")
                    draw_rank_card.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill="white")

                    # Progress Bar Fill
                    progress = float(current_xp / level_end_xp)

                    if progress <= 0:
                        progress = 0.01
                    elif progress > 1:
                        progress = 1

                    w *= progress

                    draw_rank_card.ellipse((x + w, y, x + h + w, y + h), fill=0x006eff)
                    draw_rank_card.ellipse((x, y, x + h, y + h), fill=0x006eff)
                    draw_rank_card.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=0x006eff)

                    rank_card.save('card.png')

                    await ctx.send(file=discord.File('card.png'))
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

        members_long_list = []

        for stat in levels:
            member = ctx.message.guild.get_member(stat[0])

            members_long_list.append(member)

        member_names = []

        for m_name in [m.name for m in members_long_list]:
            member_names.append(m_name)

        first_place = member_names[0]

        second_place = member_names[1]

        third_place = member_names[2]

        fourth_place = member_names[3]

        fifth_place = member_names[4]

        sixth_place = member_names[5]

        seventh_place = member_names[6]

        eighth_place = member_names[7]

        ninth_place = member_names[8]

        tenth_place = member_names[9]

        lb_embed = discord.Embed(title=f"{ctx.message.guild.name} Levelling Leaderboard", colour=0xa6f7ff)
        lb_embed.add_field(name=f":first_place: #1", value=f"{first_place}", inline=False)
        lb_embed.add_field(name=f":second_place: #2", value=f"{second_place}", inline=False)
        lb_embed.add_field(name=f":third_place: #3", value=f"{third_place}", inline=False)
        lb_embed.add_field(name=f"#4", value=f"{fourth_place}", inline=False)
        lb_embed.add_field(name=f"#5", value=f"{fifth_place}", inline=False)
        lb_embed.add_field(name=f"#6", value=f"{sixth_place}", inline=False)
        lb_embed.add_field(name=f"#7", value=f"{seventh_place}", inline=False)
        lb_embed.add_field(name=f"#8", value=f"{eighth_place}", inline=False)
        lb_embed.add_field(name=f"#9", value=f"{ninth_place}", inline=False)
        lb_embed.add_field(name=f"#10", value=f"{tenth_place}", inline=False)

        await ctx.send(embed=lb_embed)


def setup(hartex):
    hartex.add_cog(LevellingSystem(hartex))
