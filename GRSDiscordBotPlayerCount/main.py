import a2s
import discord
import asyncio
import os
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN_PLAYERCOUNT")
SERVER_ADDRESS = ('173.234.108.146', 24003)
WAIT_TIME = 60

client = discord.Client()

@client.event
async def on_ready():
    print(f"Bot is ready as {client.user}".format(client))
    status_task.start()

@tasks.loop()
async def status_task() -> None:
    info = a2s.info(SERVER_ADDRESS)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{info.player_count}/{info.max_players} Players".format(info=info)))
    await asyncio.sleep(WAIT_TIME)


client.run(DISCORD_TOKEN)