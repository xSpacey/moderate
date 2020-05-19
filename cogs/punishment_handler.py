from discord.ext import commands, tasks
from discord.utils import get

import database.database_sqlite3 as db
from config import LOG_UNBANS, LOG_UNMUTES
from utils.punishment import can_unpunish


class PunishmentHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.monitor_punishments.start()

    def cog_unload(self):
        self.monitor_punishments.cancel()

    @tasks.loop(seconds=15)
    async def monitor_punishments(self):
        await self.bot.wait_until_ready()

        for ban in db.get_current_bans():
            """
            [0]: Unban date
            [1]: User ID
            [2]: Guild ID
            [3]: Row ID
            """
            if can_unpunish(ban[0]):
                guild = await self.bot.fetch_guild(ban[2])
                user = await self.bot.fetch_user(ban[1])
                db.expire_ban(ban[3])
                await guild.unban(user)
                if LOG_UNBANS:
                    await self.bot.get_cog('Logs').log("INFO", f"{user} has been unbanned as their ban has expired.")

        for mute in db.get_current_mutes():
            """
            [0]: Unmute date
            [1]: User ID
            [2]: Guild ID
            [3]: Row ID
            """
            if can_unpunish(mute[0]):
                guild = self.bot.get_guild(mute[2])
                member = guild.get_member(mute[1])
                db.expire_mute(mute[3])
                await member.remove_roles(get(guild.roles, name="Muted"))
                if LOG_UNMUTES:
                    await self.bot.get_cog('Logs').log("INFO", f"{member} has been unmuted as their mute has expired.")

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        if db.currently_muted(ctx.id):
            await ctx.add_roles(get(ctx.guild.roles, name="Muted"))


def setup(bot):
    bot.add_cog(PunishmentHandler(bot))
