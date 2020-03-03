import discord
from discord.ext import commands
from discord import Embed

from core.classes import *


class Global(CategoryExtension):

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def ping(self, ctx):
        await ctx.send(f"Hey, it's me, HarTex! :eyes: Did you need something? - `{str(round(self.bot.latency * 1000))} ms`")

    @commands.command()
    async def about(self, ctx):
        about_me = discord.Embed(colour=0xa6f7ff)
        about_me.set_author(name="HarTex", icon_url="https://media.discordapp.net/attachments/582782144099778560/680318768907419668/your_profile_picture.jpg?width=450&height=450")
        about_me.description = "HarTex is a bot meant for servers with advanced moderation needs, run by Harry.#2450 and maintained by the HarTex Development Team."
        about_me.add_field(name="Whitelisted Servers", value=str(len(self.bot.guilds)), inline=False)

        await ctx.send(embed=about_me)

    @commands.command()
    async def help(self, ctx, command=None):
        """
        .help

        A custom help command.
        """
        if command is None:
            helpEmbed = Embed(title="HarTex Help", description="Common Moderation Commands",
                              footer="Execute `help <command>` to get more information about one command.",
                              colour=0xa6f7ff)
            helpEmbed.add_field(name="kick", value="Kicks a user.", inline=False)
            helpEmbed.add_field(name="ban", value="Bans a user.", inline=False)
            helpEmbed.add_field(name="unban", value="Unbans a user.", inline=False)
            helpEmbed.add_field(name="mute", value="Mutes a user.", inline=False)
            helpEmbed.add_field(name="unmute", value="Unmutes a user.", inline=False)
            helpEmbed.add_field(name="tempmute", value="Temporarily mutes a user.", inline=False)

            await ctx.send(embed=helpEmbed)
        elif command == "kick":
            helpKickEmbed = Embed(title="HarTex Help: Kick", description="Kick: Usage", colour=0xa6f7ff)
            helpKickEmbed.add_field(name="Usage", value="kick <member: **discord.Member**> <reason: **optional**>",
                                    inline=False)
            helpKickEmbed.add_field(name="Description", value="Kicks a member.", inline=False)

            await ctx.send(embed=helpKickEmbed)
        elif command == "ban":
            helpBanEmbed = Embed(title="HarTex Help: Ban", description="Ban: Usage", colour=0xa6f7ff)
            helpBanEmbed.add_field(name="Usage", value="ban <member: **discord.Member**> <reason: **optional**>",
                                   inline=False)
            helpBanEmbed.add_field(name="Description", value="Bans a member.", inline=False)

            await ctx.send(embed=helpBanEmbed)
        elif command == "unban":
            helpUnbanEmbed = Embed(title="HarTex Help: Unban", description="Unban: Usage", colour=0xa6f7ff)
            helpUnbanEmbed.add_field(name="Usage", value="unban <member: **discord.Member**> <reason: **optional**>",
                                     inline=False)
            helpUnbanEmbed.add_field(name="Description", value="Unbans a member.", inline=False)

            await ctx.send(embed=helpUnbanEmbed)
        elif command == "mute":
            helpMuteEmbed = Embed(title="HarTex Help: Mute", description="Mute: Usage", colour=0xa6f7ff)
            helpMuteEmbed.add_field(name="Usage", value="mute <member: **discord.Member**> <reason: **optional**>",
                                    inline=False)
            helpMuteEmbed.add_field(name="Description", value="Mutes a member.", inline=False)

            await ctx.send(embed=helpMuteEmbed)
        elif command == "unmute":
            helpUnmuteEmbed = Embed(title="HarTex Help: Unmute", description="Unmute: Usage", colour=0xa6f7ff)
            helpUnmuteEmbed.add_field(name="Usage", value="unmute <member: **discord.Member**> <reason: **optional**>",
                                      inline=False)
            helpUnmuteEmbed.add_field(name="Description", value="Unmutes a member.", inline=False)

            await ctx.send(embed=helpUnmuteEmbed)
        elif command == "tempmute":
            helpTempmuteEmbed = Embed(title="HarTex Help: Tempmute", description="Tempmute: Usage", colour=0xa6f7ff)
            helpTempmuteEmbed.add_field(name="Usage",
                                        value="tempmute <member: **discord.Member**> <time: **string**> <reason: **optional**>",
                                        inline=False)
            helpTempmuteEmbed.add_field(name="Description", value="Temporarily mutes a member.", inline=False)

            await ctx.send(embed=helpTempmuteEmbed)

    @commands.command()
    async def staff(self, ctx):
        staff_embed = discord.Embed(colour=0xa6f7ff)
        staff_embed.set_author(name="HarTex Staff",
                               icon_url="https://media.discordapp.net/attachments/582782144099778560/680318768907419668/your_profile_picture.jpg?width=450&height=450")
        staff_embed.description = "Without the people above, this bot cannot be this great!"
        staff_embed.add_field(name="Global Administrator & Developer", value="Harry.#2450", inline=False)
        staff_embed.add_field(name="Lead Developer", value="Harry.#2450", inline=False)
        staff_embed.add_field(name="Development Team", value="OfficialAz3#0762", inline=False)
        staff_embed.add_field(name="HarTex Support Team", value="Harry.#2450\nOfficialAz3#0762", inline=False)

        await ctx.send(embed=staff_embed)


def setup(hartex):
    hartex.add_cog(Global(hartex))
