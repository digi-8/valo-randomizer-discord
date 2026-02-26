# Valorant Randomizer Discord Bot

## Project Purpose
A Discord bot built in Python as a learning project. The bot randomizes Valorant agents and maps for players in a voice channel.

## Core Features

### 1. Agent Randomizer
- Detects all members currently in a voice channel
- Splits members into two teams (or handles uneven teams gracefully)
- Assigns each player a random Valorant agent
- **Key constraint**: No two players on the same team can share the same agent
- Posts results clearly showing each player's assigned agent, grouped by team

### 2. Map Randomizer
- Randomly selects one map from the current Valorant map pool
- Posts the selected map to the channel

## Technical Decisions

### Language & Runtime
- **Python 3.10+**
- Use `discord.py` (or `py-cord`) for the Discord bot library

### Bot Commands
- Use slash commands (`/`) via Discord's application command system — more modern than prefix commands
- Example commands:
  - `/randomize` — assigns agents to all players in the invoker's voice channel
  - `/map` — picks a random map

### Data
- Store the agent list and map list as plain Python data structures (lists/dicts) in a data file
- No database needed for MVP
- Agents should be grouped by role (Duelist, Initiator, Controller, Sentinel) in case role-based logic is added later

### Project Structure
```
valo-randomizer-discord/
├── CLAUDE.md
├── .env               # Discord bot token (never commit this)
├── .gitignore
├── requirements.txt
├── bot.py             # Entry point, bot setup
├── commands/
│   ├── agents.py      # /randomize command logic
│   └── maps.py        # /map command logic
└── data/
    ├── agents.py      # Full agent list with roles
    └── maps.py        # Current map pool list
```

### Environment & Config
- Store the bot token in a `.env` file and load it with `python-dotenv`
- Never hardcode secrets

## Constraints & Rules
- The agent pool for assignment must not repeat agents within the same team
- If a voice channel has more players than available agents, the bot should handle this gracefully (warn the user)
- Only the players present in a voice channel at the time of the command are included

## Learning Goals (Python Concepts This Project Covers)
- `async`/`await` — Discord bots are async by nature
- Lists, dicts, and data structures
- `random` module (`random.choice`, `random.shuffle`, `random.sample`)
- Modules and packages (splitting code into files)
- Environment variables and `.env` files
- Working with a third-party library (`discord.py`)
- Basic error handling

## Dependencies
```
discord.py>=2.0
python-dotenv
```
