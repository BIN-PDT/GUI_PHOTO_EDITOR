import customtkinter as ctk
from settings import *
from widgets import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # SETUP.
        ctk.set_appearance_mode("dark")
        self.geometry("1080x600")
        self.minsize(800, 500)
        self.title("")
        # LAYOUT.
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3, uniform="A")
        self.columnconfigure(1, weight=7, uniform="A")
        # WIDGET.
        ImageLoader(self, self.load_image)

    def load_image(self, path):
        print(path)


if __name__ == "__main__":
    App().mainloop()
