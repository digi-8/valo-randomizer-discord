import random
import discord
from data.agents import ALL_AGENTS


def assign_agents(team1, team2):
    """Randomly assign agents to players with no duplicates within each team."""
    agents_pool = ALL_AGENTS.copy()
    random.shuffle(agents_pool)

    assignments = {}
    used_team1 = set()
    used_team2 = set()

    for player in team1:
        available = [a for a in agents_pool if a not in used_team1]
        agent = random.choice(available)
        assignments[player] = agent
        used_team1.add(agent)

    for player in team2:
        available = [a for a in agents_pool if a not in used_team2]
        agent = random.choice(available)
        assignments[player] = agent
        used_team2.add(agent)

    return assignments


def format_result(team1, team2, assignments):
    """Build the formatted message string from assignments."""
    lines = ["**Agent Randomizer**\n"]

    lines.append("**Team 1**")
    for player in team1:
        lines.append(f"  {player.display_name} → {assignments[player]}")

    if team2:
        lines.append("\n**Team 2**")
        for player in team2:
            lines.append(f"  {player.display_name} → {assignments[player]}")

    return "\n".join(lines)


class RerollButton(discord.ui.Button):
    def __init__(self, player, team_num):
        super().__init__(label=f"↺ {player.display_name}", style=discord.ButtonStyle.secondary)
        self.player = player
        self.team_num = team_num

    async def callback(self, interaction: discord.Interaction):
        view: RerollView = self.view

        # Find which agents are already taken by this player's teammates
        team = view.team1 if self.team_num == 1 else view.team2
        teammates = [p for p in team if p != self.player]
        used_by_team = {view.assignments[p] for p in teammates}

        available = [a for a in ALL_AGENTS if a not in used_by_team]
        new_agent = random.choice(available)
        old_agent = view.assignments[self.player]
        view.assignments[self.player] = new_agent

        print(f"[Reroll] {interaction.user.display_name} rerolled {self.player.display_name}: {old_agent} → {new_agent}")

        result = format_result(view.team1, view.team2, view.assignments)
        await interaction.response.edit_message(content=result, view=view)


class RerollView(discord.ui.View):
    def __init__(self, team1, team2, assignments):
        super().__init__(timeout=None)
        self.team1 = team1
        self.team2 = team2
        self.assignments = assignments

        for player in team1:
            self.add_item(RerollButton(player, 1))
        for player in team2:
            self.add_item(RerollButton(player, 2))


class TeamSelectView(discord.ui.View):
    """Dropdown that lets the user pick who goes on Team 1."""

    def __init__(self, players):
        super().__init__()
        self.players = players

        select = discord.ui.Select(
            placeholder="Select Team 1 players...",
            min_values=1,
            max_values=len(players) - 1,
            options=[
                discord.SelectOption(label=p.display_name, value=str(p.id))
                for p in players
            ],
        )
        select.callback = self.on_select
        self.add_item(select)

    async def on_select(self, interaction: discord.Interaction):
        selected_ids = set(self.children[0].values)
        team1 = [p for p in self.players if str(p.id) in selected_ids]
        team2 = [p for p in self.players if str(p.id) not in selected_ids]

        assignments = assign_agents(team1, team2)
        result = format_result(team1, team2, assignments)
        view = RerollView(team1, team2, assignments)

        # Dismiss the ephemeral team picker and post the result publicly
        await interaction.response.edit_message(content="Teams set!", view=None)
        await interaction.followup.send(result, view=view)


async def handle_randomize(interaction: discord.Interaction, mode: str = "auto"):
    # Check the user is in a voice channel
    if interaction.user.voice is None:
        await interaction.response.send_message("You need to be in a voice channel first.", ephemeral=True)
        return

    members = interaction.user.voice.channel.members
    players = [m for m in members if not m.bot]

    if len(players) == 0:
        await interaction.response.send_message("No players found in your voice channel.", ephemeral=True)
        return

    if len(players) > len(ALL_AGENTS):
        await interaction.response.send_message(
            f"Too many players ({len(players)}) — only {len(ALL_AGENTS)} agents available.",
            ephemeral=True,
        )
        return

    if mode == "manual":
        if len(players) < 2:
            await interaction.response.send_message("Need at least 2 players to pick teams manually.", ephemeral=True)
            return

        view = TeamSelectView(players)
        await interaction.response.send_message(
            "Select the players for **Team 1** — everyone else goes to Team 2:",
            view=view,
            ephemeral=True,
        )
    else:
        # Auto mode: bot splits teams randomly
        random.shuffle(players)
        mid = len(players) // 2
        team1 = players[:mid] if len(players) > 1 else players
        team2 = players[mid:] if len(players) > 1 else []

        assignments = assign_agents(team1, team2)
        result = format_result(team1, team2, assignments)
        view = RerollView(team1, team2, assignments)
        await interaction.response.send_message(result, view=view)
