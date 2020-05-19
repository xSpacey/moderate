from discord.ext import commands

from config import LOGGING_CHANNEL, LOG_JOIN, LOG_LEAVE
from utils.punishment import get_datetime


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = self.bot.get_channel(LOGGING_CHANNEL)

    async def log(self, prefix, message):
        await self.log_channel.send(f"**[{prefix}]** {message}")

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        if LOG_JOIN:
            await self.log("INFO", f"{ctx} has joined the server at {get_datetime()}")

    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        if LOG_LEAVE:
            await self.log("INFO", f"{ctx} has left the server at {get_datetime()}")


def setup(bot):
    bot.add_cog(Logs(bot))
