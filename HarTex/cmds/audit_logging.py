import discord
from discord.ext import commands

from core.classes import *

import yaml


class Logging(CategoryExtension):

    # Member Actions

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        memberGuild = member.guild

        def get_channel_id():
            with open(f'configurations/{memberGuild.id}_config.yaml', 'r') as channel_accessor:
                member_log = yaml.safe_load(channel_accessor)

                channel_id: discord.TextChannel = memberGuild.get_channel(member_log['plugins']['logging']['type']['member_log']['channel'])

            return channel_id

        MemberLogChannel = get_channel_id()

        JoinEmbed = discord.Embed(title=":inbox_tray: Member Joined", colour=0xa6f7ff)
        JoinEmbed.add_field(name="Member", value=member.mention, inline=False)
        JoinEmbed.set_thumbnail(url=member.avatar_url)

        await MemberLogChannel.send(embed=JoinEmbed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        memberGuild = member.guild

        def get_channel_id():
            with open(f'configurations/{memberGuild.id}_config.yaml', 'r') as channel_accessor:
                member_log = yaml.safe_load(channel_accessor)

                channel_id: discord.TextChannel = memberGuild.get_channel(
                    member_log['plugins']['logging']['type']['member_log']['channel'])

            return channel_id

        MemberLogChannel = get_channel_id()

        LeaveEmbed = discord.Embed(title=":outbox_tray: Member Left", colour=0xa6f7ff)
        LeaveEmbed.add_field(name="Member", value=member.mention, inline=False)
        LeaveEmbed.set_thumbnail(url=member.avatar_url)

        await MemberLogChannel.send(embed=LeaveEmbed)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        memberGuild = before.guild

        def get_channel_id():
            with open(f'configurations/{memberGuild.id}_config.yaml', 'r') as channel_accessor:
                member_log = yaml.safe_load(channel_accessor)

                channel_id: discord.TextChannel = memberGuild.get_channel(
                    member_log['plugins']['logging']['type']['member_log']['channel'])

            return channel_id

        MemberLogChannel = get_channel_id()

        if before.nick != after.nick:
            NicknameEmbed = discord.Embed(title=f":name_badge: {before.name} Changed Nickname", colour=0xa6f7ff)
            NicknameEmbed.add_field(name="Before", value=f"`{before.nick}`", inline=True)
            NicknameEmbed.add_field(name="After", value=f"`{after.nick}`", inline=True)

            await MemberLogChannel.send(embed=NicknameEmbed)
        elif before.roles != after.roles:
            def difference_between_list(list1, list2):
                listDifference = [item for item in list1 + list2 if item not in list1 or item not in list2]
                return listDifference

            roleDifference = difference_between_list(before.roles, after.roles)

            if len(before.roles) < len(after.roles):
                RolesEmbed = discord.Embed(title=f":key: A Role Has Been Given To {before.name}", colour=0xa6f7ff)
                RolesEmbed.add_field(name="Role Added", value="{}".join(role.mention for role in roleDifference).replace("{}", "\n"), inline=False)

                await MemberLogChannel.send(embed=RolesEmbed)
            elif len(before.roles) > len(after.roles):
                RolesEmbed = discord.Embed(title=f":key: A Role Has Been Removed From {before.name}", colour=0xa6f7ff)
                RolesEmbed.add_field(name="Role Removed",
                                     value="{}".join(role.mention for role in roleDifference).replace("{}", "\n"),
                                     inline=False)

                await MemberLogChannel.send(embed=RolesEmbed)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        for guild in self.bot.guilds:
            if guild.get_member(before.id) is None:
                continue
            else:
                def get_channel_id():
                    with open(f'configurations/{guild.id}_config.yaml', 'r') as id_accessor:
                        ID = yaml.safe_load(id_accessor)

                        id_string: discord.TextChannel = guild.get_channel(ID['plugins']['logging']['type']['member_log']['channel'])

                    return id_string

                MemberLoggingChannel = get_channel_id()
        
                if before.avatar != after.avatar:
                    AvatarEmbed = discord.Embed(title=f":pencil: {before.name} Changed His/Her Avatar", colour=0xa6f7ff)
                    AvatarEmbed.set_thumbnail(url=after.avatar_url)

                    await MemberLoggingChannel.send(embed=AvatarEmbed)
                elif before.name != after.name:
                    NameEmbed = discord.Embed(title=f":pencil: {after.name} Changed His/Her Username", colour=0xa6f7ff)
                    NameEmbed.add_field(name="Before", value=f"{before.name}", inline=True)
                    NameEmbed.add_field(name="After", value=f"{after.name}", inline=False)

                    await MemberLoggingChannel.send(embed=NameEmbed)
                elif before.discriminator != after.discriminator:
                    DiscriminatorEmbed = discord.Embed(title=f":pencil: {after.name} Changed His/Her Username", colour=0xa6f7ff)
                    DiscriminatorEmbed.add_field(name="Before", value=f"{before.discriminator}", inline=True)
                    DiscriminatorEmbed.add_field(name="After", value=f"{after.discriminator}", inline=False)

                    await MemberLoggingChannel.send(embed=DiscriminatorEmbed)

    # Message Actions

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        messageGuild = before.guild

        def get_channel_id():
            with open(f'configurations/{messageGuild.id}_config.yaml', 'r') as channel_accessor:
                member_log = yaml.safe_load(channel_accessor)

                channel_id: discord.TextChannel = messageGuild.get_channel(
                    member_log['plugins']['logging']['type']['message_log']['channel'])

            return channel_id

        MessageLogChannel = get_channel_id()

        EditEmbed = discord.Embed(title=":pencil: Message Edited", colour=0xa6f7ff)
        EditEmbed.add_field(name="Message Edited By", value=before.author.mention, inline=False)
        EditEmbed.add_field(name="Message Channel", value=f"{before.channel}", inline=False)
        EditEmbed.add_field(name="Before", value=f"{before.content}", inline=True)
        EditEmbed.add_field(name='After', value=f"{after.content}", inline=True)

        if after.author.bot:
            return

        await MessageLogChannel.send(embed=EditEmbed)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        messageGuild = message.guild

        def get_channel_id():
            with open(f'configurations/{messageGuild.id}_config.yaml', 'r') as channel_accessor:
                member_log = yaml.safe_load(channel_accessor)

                channel_id: discord.TextChannel = messageGuild.get_channel(
                    member_log['plugins']['logging']['type']['message_log']['channel'])

            return channel_id

        MessageLogChannel = get_channel_id()

        DeleteEmbed = discord.Embed(title=":wastebasket: Message Deleted", colour=0xa6f7ff)
        DeleteEmbed.add_field(name="Message Sent By", value=message.author.mention, inline=False)
        DeleteEmbed.add_field(name="Message Channel", value=f"{message.channel}", inline=False)
        DeleteEmbed.add_field(name="Content", value=f"{message.content}", inline=True)

        if message.author.bot:
            return

        await MessageLogChannel.send(embed=DeleteEmbed)

    # Guild Actions

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.TextChannel):
        channelGuild = channel.guild

        def get_channel_id():
            with open(f'configurations/{channelGuild.id}_config.yaml', 'r') as channel_accessor:
                member_log = yaml.safe_load(channel_accessor)

                channel_id: discord.TextChannel = channelGuild.get_channel(
                    member_log['plugins']['logging']['type']['message_log']['channel'])

            return channel_id

        ChannelsLogChannel = get_channel_id()

        ChannelCreateEmbed = discord.Embed(title=":white_check_mark: Text Channel Created", colour=0xa6f7ff)
        ChannelCreateEmbed.add_field(name="Channel Name", value=f"{channel.name}", inline=False)
        ChannelCreateEmbed.add_field(name="Channel Topic", value=f"{channel.topic}", inline=False)
        ChannelCreateEmbed.add_field(name="Channel Category", value=f"{channel.category}", inline=False)
        ChannelCreateEmbed.add_field(name="Permission Overrides for", value=f"{channel.overwrites}", inline=False)

        await ChannelsLogChannel.send(embed=ChannelCreateEmbed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.TextChannel):
        channelGuild = channel.guild

        def get_channel_id():
            with open(f'configurations/{channelGuild.id}_config.yaml', 'r') as channel_accessor:
                member_log = yaml.safe_load(channel_accessor)

                channel_id: discord.TextChannel = channelGuild.get_channel(
                    member_log['plugins']['logging']['type']['message_log']['channel'])

            return channel_id

        ChannelsLogChannel = get_channel_id()

        ChannelDeleteEmbed = discord.Embed(title=":negative_squared_cross_mark: Text Channel Deleted", colour=0xa6f7ff)
        ChannelDeleteEmbed.add_field(name="Channel Name", value=f"{channel.name}", inline=False)
        ChannelDeleteEmbed.add_field(name="Channel Topic", value=f"{channel.topic}", inline=False)
        ChannelDeleteEmbed.add_field(name="Channel Category", value=f"{channel.category}", inline=False)

        await ChannelsLogChannel.send(embed=ChannelDeleteEmbed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.TextChannel, after: discord.TextChannel):
        channelGuild = before.guild

        def get_channel_id():
            with open(f'configurations/{channelGuild.id}_config.yaml', 'r') as channel_accessor:
                member_log = yaml.safe_load(channel_accessor)

                channel_id: discord.TextChannel = channelGuild.get_channel(
                    member_log['plugins']['logging']['type']['message_log']['channel'])

            return channel_id

        ChannelsLogChannel = get_channel_id()

        if before.name != after.name:
            NameEmbed = discord.Embed(title=":pencil: A Text Channel has been updated", colour=0xa6f7ff)
            NameEmbed.add_field(name="Before", value=f"{before.name}", inline=False)
            NameEmbed.add_field(name="After", value=f"{after.name}", inline=False)

            await ChannelsLogChannel.send(embed=NameEmbed)
        elif before.topic != after.topic:
            TopicEmbed = discord.Embed(title=":pencil: A Text Channel has been updated", colour=0xa6f7ff)
            TopicEmbed.add_field(name="Channel Updated", value=f"{after.name}", inline=False)
            TopicEmbed.add_field(name="Before", value=f"{before.topic}", inline=False)
            TopicEmbed.add_field(name="After", value=f"{after.topic}", inline=False)

            await ChannelsLogChannel.send(embed=TopicEmbed)
        elif before.overwrites != after.overwrites:
            OverwritesEmbed = discord.Embed(title=":pencil: A Text Channel has been updated", colour=0xa6f7ff)
            OverwritesEmbed.add_field(name="Channel Updated", value=f"{after.name}", inline=False)
            OverwritesEmbed.add_field(name="Overwrites for", value=f"{after.overwrites}", inline=False)

            await ChannelsLogChannel.send(embed=OverwritesEmbed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        roleGuild = role.guild

        def get_channel_id():
            with open(f'configurations/{roleGuild.id}_config.yaml', 'r') as channel_accessor:
                member_log = yaml.safe_load(channel_accessor)

                channel_id: discord.TextChannel = roleGuild.get_channel(
                    member_log['plugins']['logging']['type']['message_log']['channel'])

            return channel_id

        RoleLoggingChannel = get_channel_id()

        RoleCreateEmbed = discord.Embed(title=":heavy_plus_sign: A Role is Created", colour=0xa6f7ff)
        RoleCreateEmbed.add_field(name="Role Created", value=f"{role.name}", inline=False)

        await RoleLoggingChannel.send(embed=RoleCreateEmbed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        roleGuild = role.guild

        def get_channel_id():
            with open(f'configurations/{roleGuild.id}_config.yaml', 'r') as channel_accessor:
                member_log = yaml.safe_load(channel_accessor)

                channel_id: discord.TextChannel = roleGuild.get_channel(
                    member_log['plugins']['logging']['type']['message_log']['channel'])

            return channel_id

        RoleLoggingChannel = get_channel_id()

        RoleDeleteEmbed = discord.Embed(title=":heavy_minus_sign: A Role is Deleted", colour=0xa6f7ff)
        RoleDeleteEmbed.add_field(name="Role Deleted", value=f"{role.name}", inline=False)

        await RoleLoggingChannel.send(embed=RoleDeleteEmbed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        roleGuild = before.guild

        def get_channel_id():
            with open(f'configurations/{roleGuild.id}_config.yaml', 'r') as channel_accessor:
                member_log = yaml.safe_load(channel_accessor)

                channel_id: discord.TextChannel = roleGuild.get_channel(
                    member_log['plugins']['logging']['type']['message_log']['channel'])

            return channel_id

        RoleLoggingChannel = get_channel_id()

        if before.name != after.name:
            NameEmbed = discord.Embed(title=":pencil: A role has been updated", colour=0xa6f77ff)
            NameEmbed.add_field(name="Before", value=f"{before.name}", inline=True)
            NameEmbed.add_field(name="After", value=f"{after.name}", inline=True)

            await RoleLoggingChannel.send(embed=NameEmbed)
        elif before.hoist != after.hoist:
            HoistEmbed = discord.Embed(title=":pencil: A role has been updated", colour=0xa6f7ff)
            HoistEmbed.add_field(name="Role Name", value=f"{after.name}", inline=False)
            HoistEmbed.add_field(name="Before: Hoisted", value=f"{before.hoist}", inline=True)
            HoistEmbed.add_field(name="After: Hoisted", value=f"{after.hoist}", inline=True)

            await RoleLoggingChannel.send(embed=HoistEmbed)
        elif before.mentionable != after.mentionable:
            MentionableEmbed = discord.Embed(title=":pencil: A role has been updated", colour=0xa6f7ff)
            MentionableEmbed.add_field(name="Role Name", value=f"{after.name}", inline=False)
            MentionableEmbed.add_field(name="Before: Mentionable", value=f"{before.mentionable}", inline=True)
            MentionableEmbed.add_field(name="After: Mentionable", value=f"{after.mentionable}", inline=True)

            await RoleLoggingChannel.send(embed=MentionableEmbed)
        elif before.permissions != after.permissions:
            PermissionsEmbed = discord.Embed(title=":pencil: A role has been updated", colour=0xa6f7ff)
            PermissionsEmbed.add_field(name="Role Name", value=f"{after.name}", inline=False)
            PermissionsEmbed.add_field(name="Before: Permissions", value=f"{before.permissions}", inline=True)
            PermissionsEmbed.add_field(name="After: Permissions", value=f"{after.permissions}", inline=True)

            await RoleLoggingChannel.send(embed=PermissionsEmbed)


def setup(hartex):
    hartex.add_cog(Logging(hartex))
