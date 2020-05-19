from discord.ext import commands

import database.database_sqlite3 as db
from config import TOKEN, PREFIX, COGS

bot = commands.Bot(command_prefix=PREFIX)


class Moderate(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX,
                         description="Moderation bot",
                         reconnect=True)
        self.bot = bot

    async def on_ready(self):
        for mod in COGS:
            try:
                self.load_extension(mod)
            except commands.ExtensionNotFound:
                print(f"Could not find module {mod}")
        db.setup()
        print(f"Logged in as {self.user}")


Moderate().run(TOKEN)
