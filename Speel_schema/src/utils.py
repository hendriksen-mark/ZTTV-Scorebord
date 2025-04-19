from typing import List, Dict, Tuple
import logging
import random
from .languages import get_translations, set_language

# Configure logging to include line numbers
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

MAX_CODE_RUNS = 2000
required_players = 0
max_consecutive_games = 0
max_games = 0
code_runs = 0

def get_lang():
    """
    Dynamically fetch the latest translations.
    """
    return get_translations()

def get_player_availability(availability: Dict[str, List[bool]]) -> Dict[str, int]:
    return {player: sum(avail) for player, avail in availability.items()}

def set_required_players(game_type: str) -> None:
    global required_players
    logging.debug(f"game_type: {game_type}")
    if game_type == "duo":
        required_players = 2
    elif game_type == "trio":
        required_players = 3
    elif game_type in ["squad", "beker"]:
        required_players = 4
    return required_players

def set_max_consecutive_games(game_type: str) -> None:
    global max_consecutive_games
    logging.debug(f"game_type: {game_type}")
    if game_type == "duo":
        max_consecutive_games = 3
    elif game_type == "trio":
        max_consecutive_games = 4
    elif game_type == "squad":
        max_consecutive_games = 7
    elif game_type == "beker":
        max_consecutive_games = 2
    return max_consecutive_games

def set_max_games(game_type: str) -> None:
    global max_games
    logging.debug(f"game_type: {game_type}")
    if game_type == "duo":
        max_games = 5
    elif game_type == "trio":
        max_games = 7
    elif game_type == "squad":
        max_games = 9
    elif game_type == "beker":
        max_games = 5
    return max_games
    
def create_schedule(
    locations: List[str],
    availability: Dict[str, List[bool]],
    required_players: int,
    max_consecutive_games: int,
    game_type: str,
    max_games: int
) -> Tuple[Dict[str, List[str]], int]:
    # Reset code_runs at the start of schedule creation
    global code_runs
    code_runs = 0  # Ensure it starts from 0 for each schedule generation

    home_locations = [loc for loc in locations if "THUIS" in loc]
    logging.debug(f"Generating schedule with locations: {locations}, required_players: {required_players}, max_consecutive_games: {max_consecutive_games}, max_games: {max_games}")
    
    while code_runs < MAX_CODE_RUNS:
        schedule = {loc: [] for loc in locations}
        player_matches = {player: 0 for player in availability}
        home_away_count = {player: {"home": 0, "away": 0} for player in availability}
        consecutive_games = {player: 0 for player in availability}
        try:
            for loc in locations:
                available_players = get_available_players(
                    loc, availability, player_matches, consecutive_games, max_games, max_consecutive_games, locations
                )
                if len(available_players) < required_players:
                    logging.warning(get_lang()["error_not_enough_players"].format(location=loc))
                    raise ValueError(get_lang()["error_not_enough_players"].format(location=loc))
                
                selected_players = select_players(loc, available_players, home_away_count, home_locations, required_players, max_consecutive_games)
                
                for player in selected_players:
                    home_away_count[player]["home" if loc in home_locations else "away"] += 1
                    player_matches[player] += 1
                    consecutive_games[player] += 1
                schedule[loc].extend(selected_players)
                
                reset_consecutive_games(availability, selected_players, consecutive_games)
            return schedule, code_runs
        except ValueError:
            code_runs += 1  # Increment code_runs on each retry
            continue
    raise RuntimeError(get_lang()["error_unable_to_generate_schedule"].format(
        locations=locations, players=len(availability), required_players=required_players,
        max_consecutive_games=max_consecutive_games, max_games=max_games
    ))

def reset_code_runs() -> None:
    """
    Reset the code runs counter.
    """
    global code_runs
    code_runs = 0

def get_available_players(
    loc: str,
    availability: Dict[str, List[bool]],
    player_matches: Dict[str, int],
    consecutive_games: Dict[str, int],
    max_games: int,
    max_consecutive_games: int,
    locations: List[str]  # Add locations as a parameter
) -> List[str]:
    """
    Get the list of available players for a location.

    Args:
        loc (str): The location.
        availability (Dict[str, List[bool]]): Availability of players.
        player_matches (Dict[str, int]): Number of matches played by each player.
        consecutive_games (Dict[str, int]): Number of consecutive games played by each player.
        max_games (int): Maximum games a player can play.
        max_consecutive_games (int): Maximum consecutive games a player can play.
        locations (List[str]): List of locations.

    Returns:
        List[str]: List of available players.
    """
    return [
        player for player, avail in availability.items()
        if avail[locations.index(loc)] and player_matches[player] < max_games and consecutive_games[player] < max_consecutive_games
    ]

def select_players(
    loc: str,
    available_players: List[str],
    home_away_count: Dict[str, Dict[str, int]],
    home_locations: List[str],
    required_players: int,
    max_consecutive_games: int
) -> List[str]:
    """
    Select players for a location.

    Args:
        loc (str): The location.
        available_players (List[str]): List of available players.
        home_away_count (Dict[str, Dict[str, int]]): Home and away game count for each player.
        home_locations (List[str]): List of home locations.
        required_players (int): Number of required players.
        max_consecutive_games (int): Maximum consecutive games a player can play.

    Returns:
        List[str]: List of selected players.
    """
    if loc in home_locations:
        return random.sample(
            [p for p in available_players if home_away_count[p]["home"] < max_consecutive_games], required_players
        )
    else:
        return random.sample(
            [p for p in available_players if home_away_count[p]["away"] < max_consecutive_games], required_players
        )

def reset_consecutive_games(
    availability: Dict[str, List[bool]],
    selected_players: List[str],
    consecutive_games: Dict[str, int]
) -> None:
    """
    Reset the consecutive games count for players not selected.

    Args:
        availability (Dict[str, List[bool]]): Availability of players.
        selected_players (List[str]): List of selected players.
        consecutive_games (Dict[str, int]): Number of consecutive games played by each player.
    """
    for player in availability:
        if player not in selected_players:
            consecutive_games[player] = 0

def print_schedule_table(
    schedule: Dict[str, List[str]],
    players: List[str],
    home_away_count: Dict[str, Dict[str, int]]
) -> None:
    """
    Print the schedule table and player stats.

    Args:
        schedule (Dict[str, List[str]]): Schedule of games.
        players (List[str]): List of players.
        home_away_count (Dict[str, Dict[str, int]]): Home and away game count for each player.
    """
    lang = get_lang()  # Fetch the latest translations dynamically
    header = lang["location"].ljust(10) + "".join([player.ljust(10) for player in players])
    logging.info("-" * len(header))
    logging.info(header)
    logging.info("-" * len(header))
    
    for loc, loc_players in schedule.items():
        row = loc.ljust(10)
        for player in players:
            row += ("X".ljust(10) if player in loc_players else "".ljust(10))
        logging.info(row)
    
    logging.info("-" * len(header))
    logging.info(lang["home"].ljust(10) + "".join([str(home_away_count[player]["home"]).ljust(10) for player in players]))
    logging.info(lang["away"].ljust(10) + "".join([str(home_away_count[player]["away"]).ljust(10) for player in players]))
    logging.info(lang["total"].ljust(10) + "".join([str(home_away_count[player]["home"] + home_away_count[player]["away"]).ljust(10) for player in players]))
    logging.info("-" * len(header))

def check_availability_length(
    locations: List[str],
    availability: Dict[str, List[bool]]
) -> None:
    """
    Check if locations and availability have the same length.

    Args:
        locations (List[str]): List of locations.
        availability (Dict[str, List[bool]]): Availability of players.

    Raises:
        ValueError: If the lengths do not match.
    """
    for player, avail in availability.items():
        if len(locations) != len(avail):
            raise ValueError(get_lang()["error_availability_length"].format(player=player, locations=len(locations), availabilities=len(avail)))

def check_available_players_for_location(
    locations: List[str],
    availability: Dict[str, List[bool]]
) -> None:
    """
    Check if there are enough available players for each location.

    Args:
        locations (List[str]): List of locations.
        availability (Dict[str, List[bool]]): Availability of players.

    Raises:
        ValueError: If there are not enough available players for a location.
    """
    for loc in locations:
        available_players = [player for player, avail in availability.items() if avail[locations.index(loc)]]
        if len(available_players) < required_players:
            raise ValueError(get_lang()["error_not_enough_players"].format(location=loc))

def check_locations(locations: List[str]) -> None:
    """
    Check if locations are unique and if half of the locations start with "THUIS".

    Args:
        locations (List[str]): List of locations.

    Raises:
        ValueError: If locations are not unique or if half of the locations do not start with "THUIS".
    """
    if len(locations) != len(set(locations)):
        raise ValueError(get_lang()["error_locations_unique"])  # Use language string for unique locations error
    
    thuis_count = sum(1 for loc in locations if loc.startswith("THUIS"))
    if thuis_count < len(locations) // 2:
        raise ValueError(get_lang()["error_locations_thuis"])  # Use language string for "THUIS" locations error

def main(game_type: str, locations: List[str], availability: Dict[str, List[bool]], language: str = "nl") -> None:
    """
    Main function to create and print the schedule.

    Args:
        game_type (str): The type of game.
        locations (List[str]): List of locations.
        availability (Dict[str, List[bool]]): Availability of players.
        language (str): Language code ("en" or "nl").
    """
    set_language(language)  # Set the language globally
    logging.info(f"Language set to: {language}")  # Log the language change

    # Set global variables based on game type
    set_required_players(game_type)
    set_max_consecutive_games(game_type)
    set_max_games(game_type)

    check_locations(locations)
    check_availability_length(locations, availability)
    check_available_players_for_location(locations, availability)
    try:
        schedule, code_runs = create_schedule(locations, availability, required_players, max_consecutive_games, game_type, max_games)
        logging.info(get_lang()["schedule_success"])  # Log success message
    except RuntimeError as e:
        logging.error(str(e))
        return
    players = list(availability.keys())
    home_away_count = {player: {"home": 0, "away": 0} for player in availability}
    home_locations = [loc for loc in locations if "THUIS" in loc]
    for loc in locations:
        for player in schedule[loc]:
            home_away_count[player]["home" if loc in home_locations else "away"] += 1
    print_schedule_table(schedule, players, home_away_count)
    logging.info(f"{get_lang()['recalculations']} {code_runs}")  # Use language string for recalculations
