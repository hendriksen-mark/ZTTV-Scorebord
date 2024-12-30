"""
Dit script genereert een schema voor het spelen van wedstrijden in een groep van spelers.
Het schema dat gegenereerd wordt is gebaseerd op de lay-out van de planning van de TTAPP.
Het schema wordt gegenereerd op basis van de speel locaties en beschikbaarheid van de spelers.
Het script ondersteunt verschillende game types en kan worden aangepast voor andere aantallen spelers per game.(duo: 2, trio: 3, squad: 4)
Het script houdt rekening met het aantal wedstrijden dat een speler kan spelen en het maximale aantal opeenvolgende wedstrijden dat een speler kan spelen.
Het script genereert een schema voor het seizoen en toont de resultaten in een tabel, inclusief statistieken voor elke speler.
Vul het game type in en de locaties en de namen met beschikbaarheid van de speler en voer het script uit om een schema te genereren.
Vul voor de thuis locaties "THUIS1", "THUIS2" in en voor de uit locaties de naam van de tegenstander of de plaats.(of een andere naam, bijvoorbeeld "UIT1", "UIT2")
Als een speler kan vul dan True in, anders False.(True = beschikbaar, False = niet beschikbaar, er word geen rekening gehouden met mischien beschikbaar)
Het invullen van de beschikbaarheid van de spelers en de locaties is van links naar rechts met links de eerste wedstrijd en rechts de laatste.
Het script geeft een foutmelding als er niet genoeg beschikbare spelers zijn voor een locatie.
Om dit script uit te voeren, kopieer de code en plak deze in een Python omgeving.
Of sla de code op als een Python bestand en voer het uit in een Python omgeving.
"""


game_type = "duo" # duo, trio(regulier), squad(landelijk)

locations = ["UIT10", "THUIS1", "UIT2", "THUIS2", "UIT3", "THUIS3", "UIT4", "THUIS4", "UIT5", "THUIS5"]

availability = {
    "Speler1": [True, True, True, True, True, True, True, True, True, True],
    "Speler2": [True, True, True, False, True, True, True, False, False, False],
    "Speler3": [True, True, True, True, True, False, False, True, True, True],
    "speler4": [True, True, True, False, True, True, True, True, True, True],
}

if game_type == "duo":
    required_players = 2
    max_consecutive_games = 3
    max_games = 5
elif game_type == "trio":
    required_players = 3
    max_consecutive_games = 4
    max_games = 7
else:
    required_players = 4
    max_consecutive_games = 7
    max_games = 9

#total_games = len(locations)
#total_players = len(availability)
#max_games = round((total_games * required_players) / total_players)




import random
from typing import List, Dict

code_runs = 0
MAX_CODE_RUNS = 2000

def create_schedule(locations: List[str], availability: Dict[str, List[bool]], required_players: int, max_consecutive_games: int) -> Dict[str, List[str]]:
    """
    Create a schedule for the games.

    Args:
        locations (List[str]): List of locations.
        availability (Dict[str, List[bool]]): Availability of players.
        required_players (int): Number of required players.
        max_consecutive_games (int): Maximum consecutive games a player can play.

    Returns:
        Dict[str, List[str]]: Schedule of games.
    """
    global code_runs
    home_locations = [loc for loc in locations if "THUIS" in loc]
    
    while code_runs < MAX_CODE_RUNS:
        schedule = {loc: [] for loc in locations}
        player_matches = {player: 0 for player in availability}
        home_away_count = {player: {"home": 0, "away": 0} for player in availability}
        consecutive_games = {player: 0 for player in availability}
        try:
            for loc in locations:
                available_players = get_available_players(loc, availability, player_matches, consecutive_games, max_games, max_consecutive_games)
                if len(available_players) < required_players:
                    raise ValueError(f"Not enough available players for location {loc}")
                
                selected_players = select_players(loc, available_players, home_away_count, home_locations, required_players, max_consecutive_games)
                
                for player in selected_players:
                    home_away_count[player]["home" if loc in home_locations else "away"] += 1
                    player_matches[player] += 1
                    consecutive_games[player] += 1
                schedule[loc].extend(selected_players)
                
                reset_consecutive_games(availability, selected_players, consecutive_games)
            return schedule
        except ValueError:
            code_runs += 1
            continue
    raise RuntimeError("Unable to generate a valid schedule. Please adjust the parameters and try again.")

def get_available_players(loc: str, availability: Dict[str, List[bool]], player_matches: Dict[str, int], consecutive_games: Dict[str, int], max_games: int, max_consecutive_games: int) -> List[str]:
    """
    Get the list of available players for a location.

    Args:
        loc (str): The location.
        availability (Dict[str, List[bool]]): Availability of players.
        player_matches (Dict[str, int]): Number of matches played by each player.
        consecutive_games (Dict[str, int]): Number of consecutive games played by each player.
        max_games (int): Maximum games a player can play.
        max_consecutive_games (int): Maximum consecutive games a player can play.

    Returns:
        List[str]: List of available players.
    """
    return [
        player for player, avail in availability.items()
        if avail[locations.index(loc)] and player_matches[player] < max_games and consecutive_games[player] < max_consecutive_games
    ]

def select_players(loc: str, available_players: List[str], home_away_count: Dict[str, Dict[str, int]], home_locations: List[str], required_players: int, max_consecutive_games: int) -> List[str]:
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

def reset_consecutive_games(availability: Dict[str, List[bool]], selected_players: List[str], consecutive_games: Dict[str, int]) -> None:
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

def print_schedule_table(schedule: Dict[str, List[str]], players: List[str], home_away_count: Dict[str, Dict[str, int]]) -> None:
    """
    Print the schedule table and player stats.

    Args:
        schedule (Dict[str, List[str]]): Schedule of games.
        players (List[str]): List of players.
        home_away_count (Dict[str, Dict[str, int]]): Home and away game count for each player.
    """
    header = "Locatie".ljust(10) + "".join([player.ljust(10) for player in players])
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    
    for loc, loc_players in schedule.items():
        row = loc.ljust(10)
        for player in players:
            row += ("X".ljust(10) if player in loc_players else "".ljust(10))
        print(row)
    
    print("-" * len(header))
    print("Thuis".ljust(10) + "".join([str(home_away_count[player]["home"]).ljust(10) for player in players]))
    print("Uit".ljust(10) + "".join([str(home_away_count[player]["away"]).ljust(10) for player in players]))
    print("Totaal".ljust(10) + "".join([str(home_away_count[player]["home"] + home_away_count[player]["away"]).ljust(10) for player in players]))
    print("-" * len(header))

def check_availability_length(locations: List[str], availability: Dict[str, List[bool]]) -> None:
    """
    Check if locations and availability have the same length.

    Args:
        locations (List[str]): List of locations.
        availability (Dict[str, List[bool]]): Availability of players.

    Raises:
        ValueError: If the lengths do not match.
    """
    for player, avail in availability.items():
        if len(locations) is not len(avail):
            raise ValueError(f"Invoer mismatch voor speler {player}: {len(locations)} locaties, {len(avail)} ingevoerde beschikbaarheden")

def check_available_players_for_location(locations: List[str], availability: Dict[str, List[bool]]) -> List[str]:
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
            raise ValueError(f"Niet genoeg spelers beschikbaar voor locatie {loc} ({len(available_players)} beschikbaar, {required_players} nodig)")

def check_locations(locations: List[str]) -> None:
    """
    Check if locations are unique and if half of the locations start with "THUIS".

    Args:
        locations (List[str]): List of locations.

    Raises:
        ValueError: If locations are not unique or if half of the locations do not start with "THUIS".
    """
    if len(locations) != len(set(locations)):
        raise ValueError("Locaties moeten uniek zijn.")
    
    thuis_count = sum(1 for loc in locations if loc.startswith("THUIS"))
    if thuis_count < len(locations) // 2:
        raise ValueError("Minimaal de helft van de locaties moet beginnen met 'THUIS'.")

def main() -> None:
    """
    Main function to create and print the schedule.
    """
    check_locations(locations)
    check_availability_length(locations, availability)
    check_available_players_for_location(locations, availability)
    try:
        schedule = create_schedule(locations, availability, required_players, max_consecutive_games)
    except RuntimeError as e:
        print(str(e))
        return
    players = list(availability.keys())
    home_away_count = {player: {"home": 0, "away": 0} for player in availability}
    home_locations = [loc for loc in locations if "THUIS" in loc]
    for loc in locations:
        for player in schedule[loc]:
            home_away_count[player]["home" if loc in home_locations else "away"] += 1
    print_schedule_table(schedule, players, home_away_count)
    print(f"Aantal herberekeningen: {code_runs}")

if __name__ == "__main__":
    main()
