import customtkinter as ctk
from PIL import Image, ImageTk
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
        self.loader = ImageLoader(self, self.load_image)

    def load_image(self, path):
        self.image = Image.open(path)
        self.image_tk = ImageTk.PhotoImage(self.image)
        # HIDE THE IMAGE LOADER.
        self.loader.grid_forget()
        # OPEN THE IMAGE EDITOR.
        self.editor = ImageEditor(self)
        self.resize_image()

    def resize_image(self):
        self.editor.create_image(0, 0, image=self.image_tk)


if __name__ == "__main__":
    App().mainloop()
