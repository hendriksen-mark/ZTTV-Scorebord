def get_player_availability(availability):
    return {player: sum(avail) for player, avail in availability.items()}

def get_required_players(game_type):
    if game_type == "duo":
        return 2
    elif game_type == "trio":
        return 3
    else:
        return 4

def get_max_consecutive_games(game_type):
    if game_type == "duo":
        return 3
    elif game_type == "trio":
        return 4
    else:
        return 7

def get_max_games(game_type):
    if game_type == "duo":
        return 5
    elif game_type == "trio":
        return 7
    else:
        return 9