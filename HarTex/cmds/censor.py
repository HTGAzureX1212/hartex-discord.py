import discord
from discord.ext import commands

import re

import yaml

from core.classes import *


def is_zalgo_nickname_enabled(guild_id):
    with open(f'configurations/{guild_id}_config.yaml', 'r') as zalgo_prevention_enabled:
        accessor = yaml.safe_load(zalgo_prevention_enabled)

        nickname_enabled = accessor['plugins']['censorship']['settings']['zalgo']['filter_nicknames']

        return nickname_enabled


def is_invite_enabled(guild_id):
    with open(f'configurations/{guild_id}_config.yaml', 'r') as invites_enabled:
        accessor = yaml.safe_load(invites_enabled)

        invite_enabled = accessor['plugins']['censorship']['settings']['invites']['filter']

    return invite_enabled


def is_nickname_invite_enabled(guild_id):
    with open(f'configurations/{guild_id}_config.yaml', 'r') as nickname_invites:
        accessor = yaml.safe_load(nickname_invites)

        invite_nick_enabled = accessor['plugins']['censorship']['settings']['invites']['filter_nicknames']

    return invite_nick_enabled


def is_domains_enabled(guild_id):
    with open(f'configurations/{guild_id}_config.yaml', 'r') as domains_enabled:
        accessor = yaml.safe_load(domains_enabled)

        domains = accessor['plugins']['censorship']['settings']['domains']['filter']

    return domains


def domains_list(guild_id):
    with open(f'configurations/{guild_id}_config.yaml', 'r') as domains_blacklist:
        accessor = yaml.safe_load(domains_blacklist)

        domain_list = accessor['plugins']['censorship']['settings']['domains']['filter_list']

    return domain_list


def is_domains_nickname_enabled(guild_id):
    with open(f'configurations/{guild_id}_config.yaml', 'r') as nickname_blacklist:
        accessor = yaml.safe_load(nickname_blacklist)

        nick_enabled = accessor['plugins']['censorship']['settings']['domains']['filter_nicknames']

    return nick_enabled


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

        def get_ignored_users():
            with open(f'configurations/{message_guild.id}_config.yaml', 'r') as censored_words:
                accessor = yaml.safe_load(censored_words)

                list_of_censored_words = accessor['plugins']['censorship']['settings']['blocked']['ignored_users']

            return list_of_censored_words

        censored_word = get_censored_words()

        ignored_users = get_ignored_users()

        for word in censored_word:
            if word in message.content:
                for user in ignored_users:
                    if user == message.author.id:
                        pass

                        break
                    else:
                        await message.delete()
                        await message.channel.send("Blacklisted word!")

                        break
                break
            else:
                continue


        def is_zalgo_enabled():
            with open(f'configurations/{message_guild.id}_config.yaml', 'r') as zalgo_prevention_enabled:
                accessor = yaml.safe_load(zalgo_prevention_enabled)

                enabled = accessor['plugins']['censorship']['settings']['zalgo']['filter']

            return enabled

        zalgo_enabled = is_zalgo_enabled()

        zalgo_re = re.compile(r"[\u0300-\u036F\u0489]")

        if zalgo_enabled:
            if zalgo_re.search(message.content):
                await message.delete()
                await message.channel.send("Zalgo detected!")
        else:
            pass

        invites = is_invite_enabled(message_guild.id)

        if invites:
            if 'discord.gg' in message.content:
                await message.delete()
                await message.channel.send("Invites are not allowed!")
        else:
            pass

        domains = is_domains_enabled(message_guild.id)

        domain_blacklist = domains_list(message_guild.id)

        if domains:
            for domain in domain_blacklist:
                if domain in message.content:
                    await message.delete()

                    await message.channel.send("This domain is blacklisted!")

                    break
                else:
                    continue
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

        censored_nickname = get_censored_nicknames()

        zalgo_nick_enabled = is_zalgo_nickname_enabled(member_guild.id)

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

        if zalgo_nick_enabled:
            if zalgo_nick_re.search(after.nick):
                last = before.nick

                if last:
                    await after.edit(nick=last)
                else:
                    await after.edit(nick="Zalgo Censored")
            else:
                pass

        nickname_invite = is_nickname_invite_enabled(member_guild.id)

        if nickname_invite:
            if 'discord.gg' in after.nick:
                last = before.nick

                if last:
                    await after.edit(nick=last)
                else:
                    await after.edit(nick="Invite Censored")
            else:
                pass

        domain_blacklist_enabled = is_domains_nickname_enabled(member_guild.id)

        domain_list = domains_list(member_guild.id)

        if domain_blacklist_enabled:
            for domain in domain_list:
                if domain in after.nick:
                    last = before.nick

                    if last:
                        await after.edit(nick=last)

                        break
                    else:
                        await after.edit(nick="Domain Censored")

                        break
                else:
                    continue
        else:
            pass


def setup(hartex):
    hartex.add_cog(Censor(hartex))
