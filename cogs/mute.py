import re

import discord
from discord.ext import commands
from discord.utils import get

from config import LOG_MUTES, MUTE_ROLES
from database.database_sqlite3 import insert_mute
from utils.punishment import get_time, get_date, get_readable_unpunish_date


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(*MUTE_ROLES)
    @commands.command(brief="Mutes the specified user - mute <@member> <time: 1m/1h/1d/perm> <reason>")
    async def mute(self, ctx, member: discord.Member, duration: str, *, reason: str):
        """
        :param ctx:
        :param member: Member to mute
        :param duration: Duration to mute for
        :param reason: Reason member was muted for
        :return: Temporarily mutes the user or returns exception
        """
        if member == ctx.author:
            await ctx.send("You cannot mute yourself.")
        else:
            if re.search(r'[0-9]+m', duration) is not None:
                duration = float(re.search(r'\d+', duration).group()) / 60
            elif re.search(r'[0-9]+h', duration) is not None:
                duration = float(re.search(r'\d+', duration).group())
            elif re.search(r'[0-9]+d', duration) is not None:
                duration = float(re.search(r'\d+', duration).group()) * 24
            else:
                duration = 'Never'

            if duration != 'Never':
                expiry = get_readable_unpunish_date(duration)
            else:
                expiry = duration

            embed = discord.Embed(title="Punishment Notice",
                                  description=f"You were punished by **{ctx.author.display_name}** "
                                              f"at **{get_time()}** on **{get_date()}**.",
                                  color=0xd8b630)

            embed.add_field(name="Reason", value=f"{reason}", inline=False)
            embed.add_field(name="Unmute Date", value=f"{expiry}", inline=False)
            embed.set_footer(text=f"{ctx.guild.name} Punishments")

            try:
                await member.send(embed=embed)
            except commands.CommandInvokeError:
                await ctx.send("User has direct messages disabled. Muting but no message sent.")
            finally:
                await member.add_roles(get(ctx.guild.roles, name="Muted"))
                insert_mute(member.id, ctx.author.id, duration, reason, ctx.guild.id)
                if LOG_MUTES:
                    await self.bot.get_cog('Logs').log("INFO",
                                                       f"{member} has been muted by {ctx.author.mention} for {reason}, "
                                                       f"expires {expiry}")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            return await ctx.send("Incorrect usage - mute <@member> <time: 1m/1h/1d/perm> <reason>", delete_after=5)


def setup(bot):
    bot.add_cog(Mute(bot))
