# Valo Randomizer

A Discord bot that randomizes Valorant agents and maps for players in a voice channel.

## Commands

- `/randomize` — assigns a random agent to everyone in your voice channel. Choose **Auto** to let the bot split teams, or **Manual** to pick teams yourself. Each player gets a reroll button after assignment.
- `/map` — picks a random map from the current pool.

## Setup

1. **Clone the repo**
   ```bash
   git clone git@github.com:digi-8/valo-randomizer-discord.git
   cd valo-randomizer-discord
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your bot token**

   Create a `.env` file in the root:
   ```
   DISCORD_TOKEN=your_token_here
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```
