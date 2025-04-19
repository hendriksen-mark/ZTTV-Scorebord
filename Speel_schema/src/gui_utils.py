import logging
from tkinter import Tk, StringVar, Label, OptionMenu, Frame, Grid, Entry, Button, Text
from .utils import set_required_players, set_max_consecutive_games, set_max_games, create_schedule, check_locations, check_availability_length, check_available_players_for_location, reset_code_runs
from .languages import LANGUAGES, get_language, set_language  # Import get_language and set_language

# Configure logging to include line numbers
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

class GameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Game Availability")

        self.language_var = StringVar(master)
        self.language_var.set(get_language())  # Use get_language to get the current language

        self.lang = LANGUAGES[get_language()]  # Load language strings dynamically

        self.game_type_var = StringVar(master)
        self.game_type_var.set("duo")  # default value

        self.locations = ["THUIS1", "UIT1", "THUIS2", "UIT2", "THUIS3", "UIT3", "THUIS4", "UIT4", "THUIS5", "UIT5"]

        self.max_consecutive_games_var = StringVar(master)
        self.max_consecutive_games_var.set(set_max_consecutive_games(self.game_type_var.get()))

        self.max_games_var = StringVar(master)
        self.max_games_var.set(set_max_games(self.game_type_var.get()))

        self.schedule_text_widget = None  # Initialize the schedule text widget

        self.availability = {
            "Speler1": [True, True, True, True, True, True, True, True, True, True],
            "Speler2": [True, True, True, True, True, True, True, True, True, True],
            "Speler3": [True, True, True, True, True, True, True, True, True, True],
            "speler4": [True, True, True, True, True, True, True, True, True, True],
        }

        # Store the current configuration
        self.current_config = {
            "game_type": self.game_type_var.get(),
            "locations": self.locations.copy(),
            "availability": {
                "Speler1": [True, True, True, True, True, True, True, True, True, True],
                "Speler2": [True, True, True, True, True, True, True, True, True, True],
                "Speler3": [True, True, True, True, True, True, True, True, True, True],
                "speler4": [True, True, True, True, True, True, True, True, True, True],
            },
            "max_consecutive_games": self.max_consecutive_games_var.get(),
            "max_games": self.max_games_var.get()
        }

        # Centralized UI creation
        self.build_ui()
        self.add_buttons()

        # Perform the first run with default configurations
        self.generate_schedule()

    def build_ui(self):
        """
        Build the UI components for language, game type, and availability.
        """
        # Language selection dropdown
        self.language_label = Label(self.master, text="Select Language:")
        self.language_label.grid(row=0, column=0, sticky="e", padx=1)

        self.language_menu = OptionMenu(self.master, self.language_var, *LANGUAGES.keys(), command=self.update_language)
        self.language_menu.grid(row=0, column=1, sticky="w", padx=1)

        # Game type selection dropdown
        self.game_type_label = Label(self.master, text=self.lang["select_game_type"])
        self.game_type_label.grid(row=0, column=2, sticky="e", padx=1)

        self.game_type_menu = OptionMenu(self.master, self.game_type_var, "duo", "trio", "squad", "beker", command=self.update_display)
        self.game_type_menu.grid(row=0, column=3, sticky="w", padx=1)

        # Max consecutive games dropdown
        self.max_consecutive_games_label = Label(self.master, text=self.lang["max_consecutive_games"])
        self.max_consecutive_games_label.grid(row=0, column=4, sticky="e", padx=1)

        self.max_consecutive_games_menu = OptionMenu(self.master, self.max_consecutive_games_var, *range(1, len(self.locations) + 1))
        self.max_consecutive_games_menu.grid(row=0, column=5, sticky="w", padx=1)

        # Max games dropdown
        self.max_games_label = Label(self.master, text=self.lang["max_games"])
        self.max_games_label.grid(row=0, column=6, sticky="e", padx=1)

        self.max_games_menu = OptionMenu(self.master, self.max_games_var, *range(1, len(self.locations) + 1))
        self.max_games_menu.grid(row=0, column=7, sticky="w", padx=1)

        # Locations label
        self.locations_label = Label(self.master, text=self.lang["locations"])
        self.locations_label.grid(row=2, column=0, sticky="w", padx=1)  # Adjusted to row 2

        self.create_availability_grid()

    def create_config_section(self):
        """
        Create the initial configuration section.
        """
        self.build_ui()  # Use centralized UI creation logic

    def create_availability_grid(self):
        # Ensure availability lists match the number of locations
        for player in self.availability:
            if len(self.availability[player]) < len(self.locations):
                self.availability[player].extend([True] * (len(self.locations) - len(self.availability[player])))
            elif len(self.availability[player]) > len(self.locations):
                self.availability[player] = self.availability[player][:len(self.locations)]

        self.grid_labels = {}
        self.availability_vars = {}
        self.player_entries = {}
        self.location_entries = {}

        # Add player names on top of the grid
        for j, player in enumerate(self.availability.keys()):
            entry = Entry(self.master)
            entry.insert(0, player)
            entry.grid(row=2, column=j + 2)  # Shifted to the right by 1 column
            self.player_entries[player] = entry

        for i, location in enumerate(self.locations):
            remove_button = Button(self.master, text=self.lang["remove"], command=lambda loc=location: self.remove_location(loc))
            remove_button.grid(row=i + 3, column=0)

            entry = Entry(self.master)
            entry.insert(0, location)
            entry.grid(row=i + 3, column=1)
            self.grid_labels[location] = entry
            self.location_entries[location] = entry

            for j, player in enumerate(self.availability.keys()):
                var = StringVar(self.master)
                var.set(self.lang["available"] if self.availability[player][i] else self.lang["unavailable"])
                option_menu = OptionMenu(self.master, var, self.lang["available"], self.lang["unavailable"])
                option_menu.grid(row=i + 3, column=j + 2)
                if player not in self.availability_vars:
                    self.availability_vars[player] = []
                self.availability_vars[player].append(var)

        # Add remove buttons below each player
        for j, player in enumerate(self.availability.keys()):
            remove_button = Button(self.master, text=self.lang["remove"], command=lambda ply=player: self.remove_player(ply))
            remove_button.grid(row=len(self.locations) + 4, column=j + 2)

    def remove_location(self, location):
        index = self.locations.index(location)
        self.locations.pop(index)
        for player in self.availability:
            self.availability[player].pop(index)
        self.update_grid()

    def remove_player(self, player):
        if player in self.availability:
            del self.availability[player]
        self.update_grid()

    def add_player(self):
        new_player = f"Speler{len(self.availability) + 1}"
        self.availability[new_player] = [True] * len(self.locations)
        self.update_grid()

    def add_location(self):
        new_location = f"THUIS{len(self.locations) + 1}"
        self.locations.append(new_location)
        for player in self.availability:
            self.availability[player].append(True)
        self.update_grid()
        self.check_locations()

    def check_locations(self):
        """
        Check if locations are unique and if half of the locations start with "THUIS".
        """
        if len(self.locations) != len(set(self.locations)):
            raise ValueError(self.lang["error_locations_unique"])  # Use language string for unique locations error
        
        # Skip the "THUIS" check for the 'beker' game type
        if self.game_type_var.get() != "beker":
            thuis_count = sum(1 for loc in self.locations if loc.startswith("THUIS"))
            if thuis_count < len(self.locations) // 2:
                raise ValueError(self.lang["error_locations_thuis"])  # Use language string for "THUIS" locations error

    def update_grid(self):
        """
        Update the grid layout and refresh the UI.
        """
        game_type = self.game_type_var.get()  # Preserve the selected game type
        player_names = {player: entry.get() for player, entry in self.player_entries.items() if player in self.availability}
        location_names = {location: entry.get() for location, entry in self.location_entries.items() if location in self.locations}
        self.clear_grid()

        self.build_ui()  # Use centralized UI creation logic

        if self.game_type_var.get() == "beker":
            self.locations = self.locations[:3]
        self.add_buttons()
        self.game_type_var.set(game_type)
        for player, name in player_names.items():
            self.player_entries[player].delete(0, "end")
            self.player_entries[player].insert(0, name)
        for location, name in location_names.items():
            if location in self.grid_labels:
                self.grid_labels[location].delete(0, "end")
                self.grid_labels[location].insert(0, name)
        self.check_locations()
        self.update_schedule_label_position()

    def update_schedule_label_position(self):
        if self.schedule_text_widget:
            self.schedule_text_widget.grid(row=len(self.locations) + 6, column=0, columnspan=6)

    def clear_grid(self):
        for widget in self.master.winfo_children():
            if widget != self.schedule_text_widget:  # Preserve the schedule_text_widget
                widget.destroy()

    def add_buttons(self):
        self.add_player_button = Button(self.master, text=self.lang["add_player"], command=self.add_player)
        self.add_player_button.grid(row=len(self.locations) + 4, column=0)

        self.add_location_button = Button(self.master, text=self.lang["add_location"], command=self.add_location)
        self.add_location_button.grid(row=len(self.locations) + 4, column=1)

        self.generate_button = Button(self.master, text=self.lang["generate_schedule"], command=self.generate_schedule)
        self.generate_button.grid(row=len(self.locations) + 5, column=0, columnspan=2)

    def update_display(self, selected_game_type):
        # Update the default values for max_consecutive_games and max_games based on the selected game type
        self.max_consecutive_games_var.set(set_max_consecutive_games(selected_game_type))
        self.max_games_var.set(set_max_games(selected_game_type))
        
        # Update the locations based on the selected game type
        if selected_game_type == "beker":
            self.locations = self.current_config["locations"][:3]  # Limit to 3 locations for "beker"
        else:
            self.locations = ["THUIS1", "UIT1", "THUIS2", "UIT2", "THUIS3", "UIT3", "THUIS4", "UIT4", "THUIS5", "UIT5"]  # Reset to default locations
        
        self.update_grid()  # Update the grid to reflect the changes
        
        # Regenerate and display the schedule
        self.generate_schedule()

    def update_language(self, selected_language):
        """
        Update the language of the application based on the selected language.
        """
        set_language(selected_language)  # Use set_language to update the global language
        self.lang = LANGUAGES[get_language()]  # Reload language strings dynamically
        logging.info(f"Language updated to: {selected_language}")  # Log the language change
        self.update_grid()  # Refresh the grid to apply the new language

    def update_max_values(self):
        self.max_consecutive_games_menu['menu'].delete(0, 'end')
        self.max_games_menu['menu'].delete(0, 'end')
        for i in range(1, len(self.locations) + 1):
            self.max_consecutive_games_menu['menu'].add_command(label=i, command=lambda value=i: self.max_consecutive_games_var.set(value))
            self.max_games_menu['menu'].add_command(label=i, command=lambda value=i: self.max_games_var.set(value))

    def generate_schedule(self):
        global code_runs
        try:
            # Ensure locations and availability are consistent
            locations = [entry.get() for entry in self.grid_labels.values()]
            availability = {self.player_entries[player].get(): [var.get() == self.lang["available"] for var in vars] for player, vars in self.availability_vars.items()}
            if len(locations) != len(self.locations):
                raise ValueError(self.lang["error_mismatch"])
            if any(len(avail) != len(locations) for avail in availability.values()):
                raise ValueError(self.lang["error_availability"])

            # Update current_config to reflect the latest changes
            self.current_config["locations"] = locations.copy()
            self.current_config["availability"] = {player: avail.copy() for player, avail in availability.items()}

            game_type = self.game_type_var.get()
            required_players = set_required_players(game_type)
            max_consecutive_games = int(self.max_consecutive_games_var.get())
            max_games = int(self.max_games_var.get())

            check_locations(locations)
            check_availability_length(locations, availability)
            check_available_players_for_location(locations, availability)
            schedule, code_runs = create_schedule(locations, availability, required_players, max_consecutive_games, game_type, max_games)
            logging.info(self.lang["schedule_success"])  # Log success message
            self.display_schedule(schedule, availability, code_runs)
        except ValueError as e:
            logging.error(f"ValueError: {e}")
            if self.schedule_text_widget:
                self.schedule_text_widget.config(state="normal")
                self.schedule_text_widget.delete("1.0", "end")
                self.schedule_text_widget.insert("1.0", str(e))
                self.schedule_text_widget.config(state="disabled")
                self.schedule_text_widget.grid()
        except RuntimeError as e:
            logging.error(f"RuntimeError: {e}")
            reset_code_runs()  # Reset code_runs after RuntimeError
            if self.schedule_text_widget:
                self.schedule_text_widget.config(state="normal")
                self.schedule_text_widget.delete("1.0", "end")
                self.schedule_text_widget.insert("1.0", str(e))
                self.schedule_text_widget.config(state="disabled")
                self.schedule_text_widget.grid()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            if self.schedule_text_widget:
                self.schedule_text_widget.config(state="normal")
                self.schedule_text_widget.delete("1.0", "end")
                self.schedule_text_widget.insert("1.0", f"{self.lang['unexpected_error']} {str(e)}")
                self.schedule_text_widget.config(state="disabled")
                self.schedule_text_widget.grid()

    def display_schedule(self, schedule, availability, code_runs):
        """
        Display the schedule below the configuration section.
        """
        if self.schedule_text_widget is None:
            self.schedule_text_widget = Text(self.master, wrap="none", height=20, width=100)
            self.schedule_text_widget.grid(row=len(self.locations) + 6, column=0, columnspan=6, pady=10)

        players = list(availability.keys())
        home_away_count = {player: {"home": 0, "away": 0} for player in availability}
        home_locations = [loc for loc in self.locations if "THUIS" in loc]
        for loc in self.locations:
            for player in schedule[loc]:
                home_away_count[player]["home" if loc in home_locations else "away"] += 1

        column_width = 10
        header = self.lang["location"].ljust(column_width) + "".join([player.ljust(column_width) for player in players])
        schedule_text = "-" * len(header) + "\n"
        schedule_text += header + "\n"
        schedule_text += "-" * len(header) + "\n"
        
        for loc, loc_players in schedule.items():
            row = loc.ljust(column_width)
            for player in players:
                row += ("X".ljust(column_width) if player in loc_players else "".ljust(column_width))
            schedule_text += row + "\n"
        
        schedule_text += "-" * len(header) + "\n"
        schedule_text += self.lang["home"].ljust(column_width) + "".join([str(home_away_count[player]["home"]).ljust(column_width) for player in players]) + "\n"
        schedule_text += self.lang["away"].ljust(column_width) + "".join([str(home_away_count[player]["away"]).ljust(column_width) for player in players]) + "\n"
        schedule_text += self.lang["total"].ljust(column_width) + "".join([str(home_away_count[player]["home"] + home_away_count[player]["away"]).ljust(column_width) for player in players]) + "\n"
        schedule_text += "-" * len(header) + "\n"
        schedule_text += f"{self.lang['recalculations']} {code_runs}"  # Use language string for recalculations

        self.schedule_text_widget.config(state="normal")
        self.schedule_text_widget.delete("1.0", "end")
        self.schedule_text_widget.insert("1.0", schedule_text)
        self.schedule_text_widget.config(state="disabled")
