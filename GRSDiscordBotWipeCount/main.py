import discord
import asyncio
import time
import datetime
import os
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN_WIPECOUNT")
WAIT_TIME = 60

client = discord.Bot()

@client.event
async def on_ready():
    print(f"Bot is ready as {client.user}".format(client))
    if not os.path.exists("wipeday.txt"):
        with open("wipeday.txt", "w") as f:
            f.write("0")
    client.loop.create_task(status_task())

@client.command()
async def set_wipe_timestamp(ctx: discord.ApplicationContext, timestamp: discord.Option(int, "The timestamp of the wipe in unix time")):
    if not ctx.guild_id in [855327322618331157, 782368687419817995]:
        await ctx.respond("This command can only be used in the GRS Discord", ephemeral=True)
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    if os.path.exists("wipeday.txt"):
        os.remove("wipeday.txt")
    with open("wipeday.txt", "w") as f:
        f.write(str(timestamp))
    with open("wipeday.txt", "r") as f:
        timestamp_txt = int(f.read())
    await ctx.respond(f"Set the wipe timestamp to {timestamp_txt}".format(timestamp_txt=timestamp_txt), ephemeral=True)
    print("Updated wipe timestamp")

async def status_task():
    while True:
        with open("wipeday.txt", "r") as f:
            wipe_timestamp = int(f.read())
        status_datetime = datetime.datetime.fromtimestamp(wipe_timestamp)
        days = (status_datetime - datetime.datetime.now()).days
        hours = (status_datetime - datetime.datetime.now()).seconds // 3600
        minutes = ((status_datetime - datetime.datetime.now()).seconds // 60) % 60
        if days <= 0:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name="wipe day!"))
        else:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{days}d, {hours}h, {minutes}m till wipe".format(days=days, hours=hours, minutes=minutes)))
        await asyncio.sleep(WAIT_TIME)

client.run(DISCORD_TOKEN)