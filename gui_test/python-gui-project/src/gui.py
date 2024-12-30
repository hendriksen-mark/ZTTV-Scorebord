from tkinter import Tk, StringVar, Label, OptionMenu, Frame, Grid, Entry, Button
from speel_schema_generator import create_schedule, check_locations, check_availability_length, check_available_players_for_location, code_runs
from utils import get_required_players, get_max_consecutive_games, get_max_games

class GameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Game Availability")

        self.game_type_var = StringVar(master)
        self.game_type_var.set("duo")  # default value

        self.game_type_label = Label(master, text="Select Game Type:")
        self.game_type_label.grid(row=0, column=0)

        self.game_type_menu = OptionMenu(master, self.game_type_var, "duo", "trio", "squad", command=self.update_display)
        self.game_type_menu.grid(row=0, column=1)

        self.locations_label = Label(master, text="Locations:")
        self.locations_label.grid(row=1, column=0, sticky="w")

        self.create_availability_grid()

        self.add_player_button = Button(master, text="Add Player", command=self.add_player)
        self.add_player_button.grid(row=len(self.locations) + 2, column=0)

        self.add_location_button = Button(master, text="Add Location", command=self.add_location)
        self.add_location_button.grid(row=len(self.locations) + 2, column=1)

        self.generate_button = Button(master, text="Generate Schedule", command=self.generate_schedule)
        self.generate_button.grid(row=len(self.locations) + 3, column=0, columnspan=2)

        self.schedule_label = Label(master, text="", justify="left")
        self.schedule_label.grid(row=len(self.locations) + 4, column=0, columnspan=2)
        self.schedule_label.grid_remove()  # Hide the schedule label initially

    def create_availability_grid(self):
        self.locations = ["UIT1", "THUIS1", "UIT2", "THUIS2", "UIT3", "THUIS3", "UIT4", "THUIS4", "UIT5", "THUIS5"]
        self.availability = {
            "Speler1": [True, True, True, True, True, True, True, True, True, True],
            "Speler2": [True, True, True, False, True, True, True, False, False, False],
            "Speler3": [True, True, True, True, True, False, False, True, True, True],
            "speler4": [True, True, True, False, True, True, True, True, True, True],
        }

        self.grid_labels = {}
        self.availability_vars = {}
        self.player_entries = {}
        self.location_entries = {}

        # Add player names on top of the grid
        for j, player in enumerate(self.availability.keys()):
            entry = Entry(self.master)
            entry.insert(0, player)
            entry.grid(row=1, column=j + 1)
            self.player_entries[player] = entry

        for i, location in enumerate(self.locations):
            entry = Entry(self.master)
            entry.insert(0, location)
            entry.grid(row=i + 2, column=0)
            self.grid_labels[location] = entry
            self.location_entries[location] = entry

            for j, player in enumerate(self.availability.keys()):
                var = StringVar(self.master)
                var.set("Available" if self.availability[player][i] else "Unavailable")
                option_menu = OptionMenu(self.master, var, "Available", "Unavailable")
                option_menu.grid(row=i + 2, column=j + 1)
                if player not in self.availability_vars:
                    self.availability_vars[player] = []
                self.availability_vars[player].append(var)

    def add_player(self):
        new_player = f"Speler{len(self.availability) + 1}"
        self.availability[new_player] = [True] * len(self.locations)
        self.player_entries[new_player] = Entry(self.master)
        self.update_grid()

    def add_location(self):
        new_location = f"LOC{len(self.locations) + 1}"
        self.locations.append(new_location)
        for player in self.availability:
            self.availability[player].append(True)
        self.location_entries[new_location] = Entry(self.master)
        self.update_grid()

    def update_grid(self):
        self.clear_grid()
        self.create_availability_grid()
        self.add_buttons()

    def clear_grid(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def add_buttons(self):
        self.add_player_button = Button(self.master, text="Add Player", command=self.add_player)
        self.add_player_button.grid(row=len(self.locations) + 2, column=0)

        self.add_location_button = Button(self.master, text="Add Location", command=self.add_location)
        self.add_location_button.grid(row=len(self.locations) + 2, column=1)

        self.generate_button = Button(self.master, text="Generate Schedule", command=self.generate_schedule)
        self.generate_button.grid(row=len(self.locations) + 3, column=0, columnspan=2)

        self.schedule_label = Label(self.master, text="", justify="left")
        self.schedule_label.grid(row=len(self.locations) + 4, column=0, columnspan=2)
        self.schedule_label.grid_remove()  # Hide the schedule label initially

    def update_display(self, selected_game_type):
        # Logic to update the display based on the selected game type can be added here
        pass

    def generate_schedule(self):
        try:
            locations = [entry.get() for entry in self.grid_labels.values()]
            availability = {self.player_entries[player].get(): [var.get() == "Available" for var in vars] for player, vars in self.availability_vars.items()}
            game_type = self.game_type_var.get()

            required_players = get_required_players(game_type)
            max_consecutive_games = get_max_consecutive_games(game_type)
            max_games = get_max_games(game_type)

            check_locations(locations)
            check_availability_length(locations, availability)
            check_available_players_for_location(locations, availability)
            schedule = create_schedule(locations, availability, required_players, max_consecutive_games)
            self.display_schedule(schedule, availability)
        except ValueError as e:
            self.schedule_label.config(text=str(e))
            self.schedule_label.grid()  # Show the schedule label
        except RuntimeError as e:
            self.schedule_label.config(text=str(e))
            self.schedule_label.grid()  # Show the schedule label
        except Exception as e:
            self.schedule_label.config(text=f"Unexpected error: {str(e)}")
            self.schedule_label.grid()  # Show the schedule label

    def display_schedule(self, schedule, availability):
        self.clear_grid()

        players = list(availability.keys())
        home_away_count = {player: {"home": 0, "away": 0} for player in availability}
        home_locations = [loc for loc in self.locations if "THUIS" in loc]
        for loc in self.locations:
            for player in schedule[loc]:
                home_away_count[player]["home" if loc in home_locations else "away"] += 1

        header = "Locatie".ljust(10) + "".join([player.ljust(10) for player in players])
        schedule_text = "-" * len(header) + "\n"
        schedule_text += header + "\n"
        schedule_text += "-" * len(header) + "\n"
        
        for loc, loc_players in schedule.items():
            row = loc.ljust(10)
            for player in players:
                row += ("X".ljust(10) if player in loc_players else "".ljust(10))
            schedule_text += row + "\n"
        
        schedule_text += "-" * len(header) + "\n"
        schedule_text += "Thuis".ljust(10) + "".join([str(home_away_count[player]["home"]).ljust(10) for player in players]) + "\n"
        schedule_text += "Uit".ljust(10) + "".join([str(home_away_count[player]["away"]).ljust(10) for player in players]) + "\n"
        schedule_text += "Totaal".ljust(10) + "".join([str(home_away_count[player]["home"] + home_away_count[player]["away"]).ljust(10) for player in players]) + "\n"
        schedule_text += "-" * len(header) + "\n"
        schedule_text += f"Aantal herberekeningen: {code_runs}"

        self.schedule_label.config(text=schedule_text)
        self.schedule_label.grid()  # Show the schedule label

        self.back_button = Button(self.master, text="Back to Config", command=self.show_config)
        self.back_button.grid(row=len(self.locations) + 5, column=0, columnspan=2)

    def show_config(self):
        self.clear_grid()
        self.create_availability_grid()
        self.add_buttons()