import random
import discord
from data.maps import MAPS


async def handle_map(interaction: discord.Interaction):
    chosen = random.choice(MAPS)
    await interaction.response.send_message(f"**Map: {chosen}**")
