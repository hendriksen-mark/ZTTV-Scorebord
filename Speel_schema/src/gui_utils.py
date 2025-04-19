import logging
from tkinter import Tk, StringVar, Label, OptionMenu, Frame, Grid, Entry, Button, Text
from .utils import set_required_players, set_max_consecutive_games, set_max_games, create_schedule, check_locations, check_availability_length, check_available_players_for_location, reset_code_runs

# Configure logging to include line numbers
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

class GameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Game Availability")

        self.game_type_var = StringVar(master)
        self.game_type_var.set("squad")  # default value

        self.locations = ["THUIS1", "UIT1", "THUIS2", "UIT2", "THUIS3", "UIT3", "THUIS4", "UIT4", "THUIS5", "UIT5"]

        self.max_consecutive_games_var = StringVar(master)
        self.max_consecutive_games_var.set(set_max_consecutive_games(self.game_type_var.get()))

        self.max_games_var = StringVar(master)
        self.max_games_var.set(set_max_games(self.game_type_var.get()))

        self.game_type_label = Label(master, text="Select Game Type:")
        self.game_type_label.grid(row=0, column=0)

        self.game_type_menu = OptionMenu(master, self.game_type_var, "duo", "trio", "squad", "beker", command=self.update_display)
        self.game_type_menu.grid(row=0, column=1)

        self.locations_label = Label(master, text="Locations:")
        self.locations_label.grid(row=1, column=0, sticky="w")

        self.availability = {
            "Speler1": [True, True, True, True, True, True, True, True, True, True],
            "Speler2": [True, True, True, True, True, True, True, True, True, True],
            "Speler3": [True, True, True, True, True, True, True, True, True, True],
            "speler4": [True, True, True, True, True, True, True, True, True, True],
        }
        self.create_availability_grid()
        self.add_buttons()

        self.schedule_text_widget = None  # Initialize the schedule text widget

        # Store the current configuration
        self.current_config = {
            "game_type": self.game_type_var.get(),
            "locations": self.locations.copy(),
            "availability": {player: avail.copy() for player, avail in self.availability.items()},
            "max_consecutive_games": self.max_consecutive_games_var.get(),
            "max_games": self.max_games_var.get()
        }

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
            entry.grid(row=1, column=j + 2)  # Shifted to the right by 1 column
            self.player_entries[player] = entry

        for i, location in enumerate(self.locations):
            remove_button = Button(self.master, text="Remove", command=lambda loc=location: self.remove_location(loc))
            remove_button.grid(row=i + 2, column=0)

            entry = Entry(self.master)
            entry.insert(0, location)
            entry.grid(row=i + 2, column=1)
            self.grid_labels[location] = entry
            self.location_entries[location] = entry

            for j, player in enumerate(self.availability.keys()):
                var = StringVar(self.master)
                var.set("Available" if self.availability[player][i] else "Unavailable")
                option_menu = OptionMenu(self.master, var, "Available", "Unavailable")
                option_menu.grid(row=i + 2, column=j + 2)
                if player not in self.availability_vars:
                    self.availability_vars[player] = []
                self.availability_vars[player].append(var)

        # Add remove buttons below each player
        for j, player in enumerate(self.availability.keys()):
            remove_button = Button(self.master, text="Remove", command=lambda ply=player: self.remove_player(ply))
            remove_button.grid(row=len(self.locations) + 3, column=j + 2)

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
            raise ValueError("Locaties moeten uniek zijn.")
        
        # Skip the "THUIS" check for the 'beker' game type
        if self.game_type_var.get() != "beker":
            thuis_count = sum(1 for loc in self.locations if loc.startswith("THUIS"))
            if thuis_count < len(self.locations) // 2:
                raise ValueError("Minimaal de helft van de locaties moet beginnen met 'THUIS'.")

    def update_grid(self):
        game_type = self.game_type_var.get()  # Preserve the selected game type
        player_names = {player: entry.get() for player, entry in self.player_entries.items() if player in self.availability}  # Preserve player names
        location_names = {location: entry.get() for location, entry in self.location_entries.items() if location in self.locations}  # Preserve location names
        self.clear_grid()
        if self.game_type_var.get() == "beker":
            self.locations = self.locations[:3]  # Ensure only 3 locations are displayed
        self.create_availability_grid()
        self.add_buttons()
        self.game_type_var.set(game_type)  # Restore the selected game type
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
        self.add_player_button = Button(self.master, text="Add Player", command=self.add_player)
        self.add_player_button.grid(row=len(self.locations) + 4, column=0)

        self.add_location_button = Button(self.master, text="Add Location", command=self.add_location)
        self.add_location_button.grid(row=len(self.locations) + 4, column=1)

        self.generate_button = Button(self.master, text="Generate Schedule", command=self.generate_schedule)
        self.generate_button.grid(row=len(self.locations) + 5, column=0, columnspan=2)

        self.max_consecutive_games_label = Label(self.master, text="Max Consecutive Games:")
        self.max_consecutive_games_label.grid(row=0, column=2)
        
        self.max_consecutive_games_menu = OptionMenu(self.master, self.max_consecutive_games_var, *range(1, len(self.locations) + 1))
        self.max_consecutive_games_menu.grid(row=0, column=3)

        self.max_games_label = Label(self.master, text="Max Games:")
        self.max_games_label.grid(row=0, column=4)

        self.max_games_menu = OptionMenu(self.master, self.max_games_var, *range(1, len(self.locations) + 1))
        self.max_games_menu.grid(row=0, column=5)

        self.game_type_label = Label(self.master, text="Select Game Type:")
        self.game_type_label.grid(row=0, column=0)

        self.game_type_menu = OptionMenu(self.master, self.game_type_var, "duo", "trio", "squad", "beker", command=self.update_display)
        self.game_type_menu.grid(row=0, column=1)

    def update_display(self, selected_game_type):
        # Update the default values for max_consecutive_games and max_games based on the selected game type
        self.max_consecutive_games_var.set(set_max_consecutive_games(selected_game_type))
        self.max_games_var.set(set_max_games(selected_game_type))
        
        # Update the locations based on the selected game type
        if selected_game_type == "beker":
            self.locations = self.current_config["locations"][:3]  # Limit to 3 locations for "beker"
        else:
            self.locations = self.current_config["locations"].copy()  # Restore the full list of locations
        
        self.update_grid()  # Update the grid to reflect the changes
        
        # Clear the schedule label and back button if they are displayed
        if self.schedule_text_widget:
            self.schedule_text_widget.grid_remove()
        if hasattr(self, 'back_button') and self.back_button.winfo_exists():
            self.back_button.grid_remove()
        if hasattr(self, 'rerun_button') and self.rerun_button.winfo_exists():
            self.rerun_button.grid_remove()

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
            availability = {self.player_entries[player].get(): [var.get() == "Available" for var in vars] for player, vars in self.availability_vars.items()}
            if len(locations) != len(self.locations):
                raise ValueError("Mismatch between locations and grid entries.")
            if any(len(avail) != len(locations) for avail in availability.values()):
                raise ValueError("Mismatch between availability and locations.")

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
            logging.info("Schedule successfully generated.")  # Log success message
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
                self.schedule_text_widget.insert("1.0", f"Unexpected error: {str(e)}")
                self.schedule_text_widget.config(state="disabled")
                self.schedule_text_widget.grid()

    def display_schedule(self, schedule, availability, code_runs):
        # Ensure the schedule_text_widget is initialized and visible
        if self.schedule_text_widget is None:
            self.schedule_text_widget = Text(self.master, wrap="none", height=20, width=100)
        self.schedule_text_widget.grid(row=len(self.locations) + 6, column=0, columnspan=6)

        self.clear_grid()
        reset_code_runs()

        players = list(availability.keys())
        home_away_count = {player: {"home": 0, "away": 0} for player in availability}
        home_locations = [loc for loc in self.locations if "THUIS" in loc]
        for loc in self.locations:
            for player in schedule[loc]:
                home_away_count[player]["home" if loc in home_locations else "away"] += 1

        column_width = 10
        header = "Locatie".ljust(column_width) + "".join([player.ljust(column_width) for player in players])
        schedule_text = "-" * len(header) + "\n"
        schedule_text += header + "\n"
        schedule_text += "-" * len(header) + "\n"
        
        for loc, loc_players in schedule.items():
            row = loc.ljust(column_width)
            for player in players:
                row += ("X".ljust(column_width) if player in loc_players else "".ljust(column_width))
            schedule_text += row + "\n"
        
        schedule_text += "-" * len(header) + "\n"
        schedule_text += "Thuis".ljust(column_width) + "".join([str(home_away_count[player]["home"]).ljust(column_width) for player in players]) + "\n"
        schedule_text += "Uit".ljust(column_width) + "".join([str(home_away_count[player]["away"]).ljust(column_width) for player in players]) + "\n"
        schedule_text += "Totaal".ljust(column_width) + "".join([str(home_away_count[player]["home"] + home_away_count[player]["away"]).ljust(column_width) for player in players]) + "\n"
        schedule_text += "-" * len(header) + "\n"
        schedule_text += f"Aantal herberekeningen: {code_runs}"

        # Update the Text widget with the schedule
        self.schedule_text_widget.config(state="normal")  # Enable editing to update the text
        self.schedule_text_widget.delete("1.0", "end")  # Clear existing text
        self.schedule_text_widget.insert("1.0", schedule_text)  # Insert new text
        self.schedule_text_widget.config(state="disabled")  # Disable editing to make it read-only

        # Add navigation buttons
        self.back_button = Button(self.master, text="Back to Config", command=self.show_config)
        self.back_button.grid(row=len(self.locations) + 7, column=0, columnspan=2)

        self.rerun_button = Button(self.master, text="Rerun", command=self.rerun_schedule)
        self.rerun_button.grid(row=len(self.locations) + 7, column=2, columnspan=2)

    def rerun_schedule(self):
        reset_code_runs()  # Reset the code_runs counter
        self.clear_grid()
        # Restore locations and availability from the current configuration
        self.locations = self.current_config["locations"].copy()
        self.availability = {player: avail.copy() for player, avail in self.current_config["availability"].items()}
        self.create_availability_grid()
        self.add_buttons()
        self.generate_schedule()

    def show_config(self):
        self.clear_grid()
        self.create_availability_grid()
        self.add_buttons()
        self.game_type_var.set(self.game_type_var.get())  # Restore the selected game type
        self.update_max_values()
        self.update_schedule_label_position()
        if self.schedule_text_widget:
            self.schedule_text_widget.grid_remove()  # Hide the schedule text widget
        if hasattr(self, 'back_button') and self.back_button.winfo_exists():
            self.back_button.grid_remove()  # Hide the back button
        if hasattr(self, 'rerun_button') and self.rerun_button.winfo_exists():
            self.rerun_button.grid_remove()  # Hide the rerun button
