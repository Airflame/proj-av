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


NOTES = {"c1": 130.81,
         "c#1": 138.59,
         "d1": 146.83,
         "d#1": 155.56,
         "e1": 164.81,
         "f1": 174.61,
         "f#1": 185.00,
         "g1": 196.00,
         "g#1": 207.65,
         "a1": 220.00,
         "a#1": 233.08,
         "b1": 246.94,
         "c2": 261.63,
         "c#2": 277.18,
         "d2": 293.66,
         "d#2": 311.13,
         "e2": 329.63,
         "f2": 349.23,
         "f#2": 369.99,
         "g2": 392.00,
         "g#2": 415.30,
         "a2": 440.00,
         "a#2": 466.16,
         "b2": 493.88,
         "c3": 523.25}

FULL_NOTE_LEN = 600


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
        elif message.content.startswith("!music"):
            await self.music(message.content.split(" ")[-1])

    async def info(self) -> None:
        await self._guild.text_channels[1].send("ProjAvTest")

    async def sound(self, freq) -> None:
        freq = max(100, freq)
        freq = min(2137, freq)
        print("Beeped {} Hz".format(freq))
        os.system("env -i beep -f {} -l 500".format(freq))
        await self._guild.text_channels[1].send("Beeped")

    async def music(self, notes_str: str) -> None:
        notes = notes_str.split("-")
        for note in notes:
            note_pitch, note_len = note.split(";")
            pitch = NOTES.get(note_pitch)
            freq = min(FULL_NOTE_LEN/float(eval(note_len)), 1000)
            freq = max(freq, 100)
            print("Played note {}".format(note_pitch))
            os.system("env -i beep -f {} -l {}".format(pitch, freq))
        await self._guild.text_channels[1].send("Played music")


client = Client(DISCORD_TOKEN, DISCORD_GUILD)
client.run()
