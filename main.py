# main.py
from tkinter import Tk
from src.gui import CaroGUI

if __name__ == "__main__":
    root = Tk()
    app = CaroGUI(root)
    root.mainloop()
