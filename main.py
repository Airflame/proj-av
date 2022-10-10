from typing import Any

import discord
import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD = os.getenv("DISCORD_GUILD")


def _get_intent() -> discord.Intents:
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    return intents


class Client(discord.Client):
    def __init__(self, token: str, guild_name: str) -> None:
        super().__init__(intents=_get_intent())

        self._token = token
        self._guild_name = guild_name

    def run(self, *args: Any, **kwargs: Any) -> None:
        super().run(self._token)

    async def on_ready(self) -> None:
        self._guild = discord.utils.get(self.guilds, name=self._guild_name)
        await self._guild.text_channels[1].send("Hello World!")

    async def on_message(self, message: discord.Message) -> None:
        if message.content.startswith("!info"):
            await self.info()
        elif message.content.startswith("!beep"):
            freq = int(message.content.split(" ")[-1])
            await self.sound(freq)

    async def info(self) -> None:
        await self._guild.text_channels[1].send("ProjAvTest")

    async def sound(self, freq) -> None:
        freq = max(100, freq)
        freq = min(2000, freq)
        print("Beeped {} Hz".format(freq))
        os.system("env -i beep -f {} -l 500".format(freq))
        await self._guild.text_channels[1].send("Beeped")


client = Client(DISCORD_TOKEN, DISCORD_GUILD)
client.run()
