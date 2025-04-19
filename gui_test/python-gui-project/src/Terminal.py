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

from typing import List, Dict
from utils import main

game_type: str = "beker"  # duo, trio(regulier), squad(landelijk), beker

locations: List[str] = ["UIT1", "THUIS1", "UIT2", "THUIS2", "UIT3", "THUIS3", "UIT4", "THUIS4", "UIT5", "THUIS5", "UIT6", "THUIS6"]

availability: Dict[str, List[bool]] = {
    "Speler1": [True, True, True, True, True, True, True, True, True, True, True, True],
    "Speler2": [True, True, True, True, True, True, True, True, True, True, True, True],
    "Speler3": [True, True, True, True, True, True, True, True, True, True, True, True],
    "speler4": [True, True, True, True, True, True, True, True, True, True, True, True],
    "speler5": [True, True, True, True, True, True, True, True, True, True, True, True],
    "speler6": [True, True, True, True, True, True, True, True, True, True, True, True],
}

if __name__ == "__main__":
    main(game_type, locations, availability)

