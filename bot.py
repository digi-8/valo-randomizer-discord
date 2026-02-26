import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="randomize", description="Assign random agents to everyone in your voice channel")
@discord.app_commands.describe(mode="How to split the teams")
@discord.app_commands.choices(mode=[
    discord.app_commands.Choice(name="Auto", value="auto"),
    discord.app_commands.Choice(name="Manual", value="manual"),
])
async def randomize(interaction: discord.Interaction, mode: str = "auto"):
    from commands.agents import handle_randomize
    await handle_randomize(interaction, mode)

@bot.tree.command(name="map", description="Pick a random Valorant map")
async def map_cmd(interaction: discord.Interaction):
    from commands.maps import handle_map
    await handle_map(interaction)

bot.run(os.getenv("DISCORD_TOKEN"))
