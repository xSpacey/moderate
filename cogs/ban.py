import re

import discord
from discord.ext import commands

from config import LOG_BANS, BAN_ROLES
from database.database_sqlite3 import insert_ban
from utils.punishment import get_time, get_date, get_readable_unpunish_date


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(*BAN_ROLES)
    @commands.command(brief="Ban the specified user - ban <@member> <time: 1m/1h/1d/perm> <reason>")
    async def ban(self, ctx, member: discord.Member, duration: str, *, reason: str):
        """
        :param ctx:
        :param member: Member to ban
        :param duration: Duration to ban for
        :param reason: Reason member was banned for
        :return: Temporarily bans the user or returns exception
        """
        if member == ctx.author:
            await ctx.send("You cannot ban yourself.")
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
            embed.add_field(name="Unban Date", value=f"{expiry}", inline=False)
            embed.set_footer(text=f"{ctx.guild.name} Punishments")

            try:
                await member.send(embed=embed)
            except commands.CommandInvokeError:
                await ctx.send("User has direct messages disabled. Banning but no message sent.")
            finally:
                await ctx.guild.ban(member, reason=reason)
                insert_ban(member.id, ctx.author.id, duration, reason, ctx.guild.id)
                if LOG_BANS:
                    await self.bot.get_cog('Logs').log("INFO",
                                                       f"{member} has been banned by {ctx.author.mention} for {reason},"
                                                       f" expires {expiry}")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            return await ctx.send("Incorrect usage - ban <@member> <time: 1m/1h/1d/perm> <reason>", delete_after=5)


def setup(bot):
    bot.add_cog(Ban(bot))
