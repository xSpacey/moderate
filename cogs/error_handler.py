from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.DisabledCommand):
            return await ctx.send("This command has been disabled.")
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(error)
        elif isinstance(error, commands.CommandNotFound):
            return


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
