import discord
from discord.ext import commands

import re

import yaml

from core.classes import *


class Censor(commands.Cog):

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        message_guild = message.guild

        def get_censored_words():
            with open(f'configurations/{message_guild.id}_config.yaml', 'r') as censored_words:
                accessor = yaml.safe_load(censored_words)

                list_of_censored_words = accessor['plugins']['censorship']['settings']['blocked']['words']

            return list_of_censored_words

        censored_word = get_censored_words()

        for word in censored_word:
            if word in message.content:
                await message.delete()
                await message.channel.send("Blacklisted word!")

                break
            else:
                continue

        def is_zalgo_enabled():
            with open(f'configurations/{message_guild.id}_config.yaml') as zalgo_prevention_enabled:
                accessor = yaml.safe_load(zalgo_prevention_enabled)

                enabled = accessor['plugins']['censorship']['setting']['zalgo']['filter']

                return enabled

        zalgo_enabled = is_zalgo_enabled()

        zalgo_re = re.compile(r"[\u0300-\u036F\u0489]")

        if zalgo_enabled == "True":
            if zalgo_re.search(message.content):
                await message.delete()
                await message.channel.send("Zalgo detected!")
        else:
            pass

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        member_guild = before.guild

        def get_censored_nicknames():
            with open(f'configurations/{member_guild.id}_config.yaml', 'r') as censored_nicknames:
                accessor = yaml.safe_load(censored_nicknames)

                list_of_censored_nicknames = accessor['plugins']['censorship']['settings']['blocked']['nicknames']

            return list_of_censored_nicknames

        def is_zalgo_nickname_enabled():
            with open(f'configurations/{member_guild.id}_config.yaml') as zalgo_prevention_enabled:
                accessor = yaml.safe_load(zalgo_prevention_enabled)

                nickname_enabled = accessor['plugins']['censorship']['settings']['zalgo']['filter_nicknames']

                return nickname_enabled

        censored_nickname = get_censored_nicknames()

        zalgo_nick_enabled = is_zalgo_nickname_enabled()

        print(zalgo_nick_enabled)

        zalgo_nick_re = re.compile(r"[\u0300-\u036F\u0489]")

        for nickname in censored_nickname:
            if nickname in after.nick:
                last = before.nick

                if last:
                    await after.edit(nick=last)
                else:
                    await after.edit(nick="Nickname Censored")

                    break
            else:
                continue

        if zalgo_nick_enabled == "True":
            if zalgo_nick_re.search(after.nick):
                last = before.nick

                if last:
                    await after.edit(nick=last)
                else:
                    await after.edit(nick="Zalgo Censored")


def setup(hartex):
    hartex.add_cog(Censor(hartex))
