from tkinter import Tk, StringVar, Label, OptionMenu, Frame, Grid

from gui import GameGUI

def main():
    root = Tk()
    root.title("Game Availability Tracker")

    game_gui = GameGUI(root)
    # game_gui.pack()  # Remove this line

    root.mainloop()

if __name__ == "__main__":
    main()