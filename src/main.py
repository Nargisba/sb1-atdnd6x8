import tkinter as tk
from gui.app import ImplantDetectorApp

def main():
    root = tk.Tk()
    app = ImplantDetectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()