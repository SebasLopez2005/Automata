FORMATION_433 = {
    "GK":  ["GK"],
    "LB":  ["LB", "LWB"],
    "CB1": ["CB"],
    "CB2": ["CB"],
    "RB":  ["RB", "RWB"],
    "CM1": ["CM", "CDM", "CAM"],
    "CM2": ["CM", "CDM", "CAM"],
    "CM3": ["CM", "CDM", "CAM"],
    "LW":  ["LW", "LM", "CF"],
    "ST":  ["ST", "CF"],
    "RW":  ["RW", "RM", "CF"],
}

def choose_best_player(players, allowed_positions, used_names):
    candidates = [
        p for p in players
        if p["position"] in allowed_positions and p["player_name"] not in used_names
    ]

    if not candidates:
        return None

    candidates.sort(key=lambda p: p["rating"], reverse=True)
    return candidates[0]

def build_starting_11(players, formation=FORMATION_433):
    lineup = {}
    used_names = set()

    for slot, allowed_positions in formation.items():
        best_player = choose_best_player(players, allowed_positions, used_names)
        lineup[slot] = best_player

        if best_player:
            used_names.add(best_player["player_name"])

    return lineup

def print_lineup(lineup):
    print("\n=== STARTING 11 ===")
    for slot, player in lineup.items():
        if player:
            print(f"{slot}: {player['player_name']} ({player['position']}) - {player['rating']}")
        else:
            print(f"{slot}: No available player")