import discord
import os
import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN_MAIN")
client = discord.Bot()

@client.event
async def on_ready():
    print(f"Bot is ready as {client.user}".format(client))

@client.command()
async def send_embed(ctx: discord.ApplicationContext, title: discord.Option(str, "The title of the embed", required=True), description: discord.Option(str, "The description of the embed", required=True), color: discord.Option(str, "The hex color of the embed", required=False)):
    if not ctx.guild_id in [855327322618331157, 782368687419817995]:
        await ctx.respond("This command can only be used in the GRS Discord", ephemeral=True)
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("You do not have permission to use this command", ephemeral=True)
        return
    description = description.replace("\\n", "\n")
    embed = discord.Embed(title=title, description=f"{description}").set_footer(text="GRS - " + datetime.datetime.now().strftime("%d/%m/%Y"))
    if color:
        embed.color = int(color, 16)
    else:
        embed.color = discord.Color.red()
    await ctx.send(embed=embed)
    await ctx.respond("Embed sent successfully", ephemeral=True)

client.run(DISCORD_TOKEN)