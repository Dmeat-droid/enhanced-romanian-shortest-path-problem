import tkinter as tk
from gui import RomaniaMapGUI


def main():
    root = tk.Tk()
    app = RomaniaMapGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()