LANGUAGES = {
    "en": {
        "select_game_type": "Select Game Type:",
        "max_consecutive_games": "Max Consecutive Games:",
        "max_games": "Max Games:",
        "locations": "Locations:",
        "generate_schedule": "Generate Schedule",
        "add_player": "Add Player",
        "add_location": "Add Location",
        "remove": "Remove",
        "schedule_success": "Schedule successfully generated!",
        "error_mismatch": "Mismatch between locations and grid entries.",
        "error_availability": "Mismatch between availability and locations.",
        "unexpected_error": "Unexpected error:",
        "rerun_schedule": "Rerun Schedule",
        "back_to_config": "Back to Config",
        "available": "Available",
        "unavailable": "Unavailable",
        "error_not_enough_players": "Not enough players available for location {location}.",
        "error_unable_to_generate_schedule": "Unable to generate schedule for:\n{locations} locations \n{players} players\n{required_players} required players\n{max_consecutive_games} max consecutive games\n{max_games} max games.",
        "error_availability_length": "Player {player} has {availabilities} availabilities, but there are {locations} locations.",
        "error_locations_unique": "Locations must be unique.",
        "error_locations_thuis": "At least half of the locations must start with 'THUIS'.",
        "recalculations": "Recalculations",
        "location": "Location",
        "home": "Home",
        "away": "Away",
        "total": "Total",
    },
    "nl": {
        "select_game_type": "Selecteer Speltype:",
        "max_consecutive_games": "Max Aaneengesloten Wedstrijden:",
        "max_games": "Max Wedstrijden:",
        "locations": "Locaties:",
        "generate_schedule": "Genereer Schema",
        "add_player": "Speler Toevoegen",
        "add_location": "Locatie Toevoegen",
        "remove": "Verwijderen",
        "schedule_success": "Schema succesvol gegenereerd!",
        "error_mismatch": "Mismatch tussen locaties en rasterinvoer.",
        "error_availability": "Mismatch tussen beschikbaarheid en locaties.",
        "unexpected_error": "Onverwachte fout:",
        "rerun_schedule": "Schema Opnieuw Uitvoeren",
        "back_to_config": "Terug naar Configuratie",
        "available": "Beschikbaar",
        "unavailable": "Niet Beschikbaar",
        "error_not_enough_players": "Niet genoeg spelers beschikbaar voor locatie {location}.",
        "error_unable_to_generate_schedule": "Kan geen schema genereren voor:\n{locations} locaties\n{players} spelers\n{required_players} vereiste spelers\n{max_consecutive_games} max opeenvolgende wedstrijden\n{max_games} max wedstrijden.",
        "error_availability_length": "Speler {player} heeft {availabilities} beschikbaarheden, maar er zijn {locations} locaties.",
        "error_locations_unique": "Locaties moeten uniek zijn.",
        "error_locations_thuis": "Minstens de helft van de locaties moet beginnen met 'THUIS'.",
        "recalculations": "Aantal herberekeningen",
        "location": "Locatie",
        "home": "Thuis",
        "away": "Uit",
        "total": "Totaal",
    },
}

_current_language = "nl"  # Default language

def set_language(language: str) -> None:
    """
    Set the current language globally.

    Args:
        language (str): Language code ("en" or "nl").
    """
    global _current_language
    _current_language = language

def get_language() -> str:
    """
    Get the current language.

    Returns:
        str: The current language code.
    """
    return _current_language

def get_translations() -> dict:
    """
    Get the translations for the current language.

    Returns:
        dict: Translations for the current language.
    """
    return LANGUAGES[_current_language]
