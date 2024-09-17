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
        # DATA.
        self.image_width = self.image_height = 0
        self.canvas_width = self.canvas_height = 0
        # WIDGET.
        self.loader = ImageLoader(self, self.load_image)

    def load_image(self, path):
        self.image = Image.open(path)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_ratio = self.image.width / self.image.height
        # HIDE THE IMAGE LOADER.
        self.loader.grid_forget()
        # OPEN THE IMAGE EDITOR.
        self.editor = ImageEditor(self, self.resize_image)

    def resize_image(self, event):
        # CURRENT RATIO.
        self.canvas_width = event.width
        self.canvas_height = event.height
        canvas_ratio = self.canvas_width / self.canvas_height
        # GET NEW WIDTH & HEIGHT OF IMAGE.
        if canvas_ratio > self.image_ratio:
            self.image_height = int(self.canvas_height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(self.canvas_width)
            self.image_height = int(self.image_width / self.image_ratio)
        # SHOW IMAGE.
        self.show_image()

    def show_image(self):
        # CUSTOMIZED IMAGE.
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        # DISCARD BEFORE DRAW.
        self.editor.delete(ctk.ALL)
        # DRAW NEW IMAGE.
        self.editor.create_image(
            self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk
        )


if __name__ == "__main__":
    App().mainloop()
