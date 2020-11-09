from typing import List, Any

import discord
import asyncio
from discord.ext import commands


class Moderator(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        description="Mutes user indefinitely",
        help="mute <user> <reason>(optional) -> mutes <user>"
    )
    @commands.has_permissions(mute_members=True)
    async def mute(self, member: discord.Member, *, reason=None):
        await member.edit(mute=True)
        if reason is None:
            await self.client.send(f"{member} was muted indefinitely")
        else:
            await self.client.send(f"{member} was muted indefinitely because: {reason}")

    @commands.command(
        name="tmpmute",
        aliases=["tmute"],
        description="Mutes user for a definite period of time",
        help="tmpmute|tmute <user> <time> <reason>(optional) -> mutes <user> for <time> minutes"
    )
    @commands.has_permissions(mute_members=True)
    async def temporary_mute(self, ctx, member: discord.Member, time, *, reason=None):
        await member.edit(mute=True)

        if reason is None:
            await self.client.send(f"{member} was muted for {int(time)} minutes")
        else:
            await self.client.send(f"{member} was muted for {int(time)} minutes because: {reason}")

        await asyncio.sleep(int(time) * 60)
        await member.edit(mute=False)

    @commands.command(
        description="Unmutes muted user",
        help="unmute <user> -> unmutes <user>"
    )
    @commands.has_permissions(mute_members=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.edit(mute=False)
        await self.client.send(f"{member} was unmuted")

    @commands.command(
        description="Kicks user from server",
        help="kick <user> <reason>(optional) -> kicks <user> from server"
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

        if reason is None:
            await self.client.send(f"{member} was kicked")
        else:
            await self.client.send(f"{member} was kicked because: {reason}")

    @commands.command(
        description="Bans user from server, kicking him, deleting all of his messages and permitting reentry",
        help="ban <user> <reason>(optional) -> bans <user> from server"
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

        if reason is None:
            await self.client.send(f"{member} was banned")
        else:
            await self.client.send(f"{member} was banned because: {reason}")

    @commands.command(
        description="Unbans user from server, reenabling him to enter the server",
        help="unban <username>#<discriminator> -> unbans user <username>#<discriminator>"
    )
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_members = await ctx.guild.bans()
        name, number = member.split('#')
        for ban_entry in banned_members:
            user = ban_entry.user
            if (user.name, user.discriminator) == (name, number):
                await ctx.guild.unban(user)
                await ctx.send(f"{member} was unbanned")
            else:
                await ctx.send(f"No such user")


def setup(client):
    client.add_cog(Moderator(client))