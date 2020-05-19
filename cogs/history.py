import discord
from discord.ext import commands

import database.database_sqlite3 as db
from config import HISTORY_ROLES
from utils.punishment import get_readable_datetime


class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_any_role(*HISTORY_ROLES)
    @commands.command(brief="Gets a users punishment history - history <member id>")
    async def history(self, ctx, member_id: int):
        """
        :param ctx:
        :param member_id: ID of the member to lookup
        :return: Embed of the member's history
        """
        member = await self.bot.fetch_user(member_id)
        bans = db.get_ban_history(member_id)
        mutes = db.get_mute_history(member_id)

        if bans == [] or mutes == []:
            await ctx.send(f"No history found for {member}.")

        else:
            embed = discord.Embed(title=f"Punishment History for {member}",
                                  color=0x50c1e2)
            embed.set_footer(text=f"{ctx.guild.name} Punishments")

            for i in bans:
                embed.add_field(name=f"**{get_readable_datetime(i[0])}**",
                                value=f"Ban - {i[5]} ({self.bot.get_user(i[2]).mention})", inline=False)
            for i in mutes:
                embed.add_field(name=f"**{get_readable_datetime(i[0])}**",
                                value=f"Mute - {i[5]} ({self.bot.get_user(i[2]).mention})", inline=False)
            await ctx.send(embed=embed)

    @history.error
    async def history_error(self, ctx, error):
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            return await ctx.send("Incorrect usage - history <member id>", delete_after=5)


def setup(bot):
    bot.add_cog(History(bot))
