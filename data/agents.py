# All agents grouped by role
# Update this list as new agents are released

AGENTS = {
    "Duelist": [
        "Jett", "Reyna", "Raze", "Phoenix", "Yoru", "Neon", "Iso", "Waylay"
    ],
    "Initiator": [
        "Sova", "Breach", "Skye", "KAY/O", "Fade", "Gekko", "Tejo"
    ],
    "Controller": [
        "Brimstone", "Viper", "Omen", "Astra", "Harbor", "Clove"
    ],
    "Sentinel": [
        "Sage", "Cypher", "Killjoy", "Chamber", "Deadlock", "Vyse"
    ],
}

# Flat list of all agents for easy sampling
ALL_AGENTS = [agent for role_agents in AGENTS.values() for agent in role_agents]
