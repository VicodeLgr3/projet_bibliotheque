import tkinter as tk


def center_window(win, width: int, height: int):
    x_coordinate = int((win.winfo_screenwidth() / 2) - (width / 2))
    y_coordinate = int((win.winfo_screenheight() / 2) - (height / 2) - 50)
    return f"{width}x{height}+{x_coordinate}+{y_coordinate}"


class Window:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Bibliothèque")
        self.window.iconbitmap('ressources/icon.ico')
        self.window.geometry(center_window(self.window, 600, 400))

        self.window.mainloop()
