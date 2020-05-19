import discord
from discord.ext import commands

from config import BLACKLISTED_URLS, LIMITED_URLS, LIMITED_URLS_CHANNELS_ALLOWED, LOG_AUTOMOD


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_content(self, message: discord.Message):
        if message.author.bot or message.guild is None:
            return

        for url in LIMITED_URLS:
            if url in message.content:
                if message.channel.id not in LIMITED_URLS_CHANNELS_ALLOWED:
                    await message.delete()
                    await message.author.send(f"The URL you sent is not allowed in {message.channel.mention}.")
                    if LOG_AUTOMOD:
                        await self.bot.get_cog('Logs').log("AUTOMOD",
                                                           f"{message.author.mention} sent '{message.content}' in "
                                                           f"{message.channel.mention}, it contained a limited URL "
                                                           f"which has now been deleted.")

        for url in BLACKLISTED_URLS:
            if url in message.content:
                await message.delete()
                await message.author.send("The URL you sent is blacklisted and may result in a ban if used again.")
                if LOG_AUTOMOD:
                    await self.bot.get_cog('Logs').log("AUTOMOD",
                                                       f"{message.author.mention} sent '{message.content}' in "
                                                       f"{message.channel.mention}, it contained a blacklisted URL "
                                                       f"which has now been deleted.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.check_content(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        if LOG_AUTOMOD:
            await self.bot.get_cog('Logs').log("AUTOMOD",
                                               f"{message.author.mention}'s message was deleted: ``{message.content}``")

    @commands.Cog.listener()
    async def on_message_edit(self, message: discord.Message, message_after: discord.Message):
        if message.author.bot:
            return
        if LOG_AUTOMOD:
            await self.bot.get_cog('Logs').log("AUTOMOD",
                                               f"{message.author.mention}'s message was edited, previously: "
                                               f"``{message.content}``")


def setup(bot):
    bot.add_cog(AutoMod(bot))
