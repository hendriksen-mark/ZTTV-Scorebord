from tkinter import Tk
from gui_utils import GameGUI

def main():
    root = Tk()
    root.title("Game Availability Tracker")
    GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()