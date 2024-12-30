import logging

# Configure logging to include line numbers
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

def get_player_availability(availability):
    return {player: sum(avail) for player, avail in availability.items()}

def get_required_players(game_type):
    logging.info(f"game_type: {game_type}")
    if game_type == "duo":
        return 2
    elif game_type == "trio":
        return 3
    else:
        return 4

def get_max_consecutive_games(game_type):
    logging.info(f"game_type: {game_type}")
    if game_type == "duo":
        return 3
    elif game_type == "trio":
        return 4
    else:
        return 7

def get_max_games(game_type):
    logging.info(f"game_type: {game_type}")
    if game_type == "duo":
        return 5
    elif game_type == "trio":
        return 7
    else:
        return 9