import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from settings import *
from widgets import *
from menu import Menu


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
        self.binding_data()
        # WIDGET.
        self.loader = ImageLoader(self, self.load_image)

    def load_image(self, path):
        self.original = Image.open(path)
        self.image = self.original.copy()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_ratio = self.image.width / self.image.height
        # HIDE THE IMAGE LOADER.
        self.loader.grid_forget()
        # OPEN THE IMAGE EDITOR.
        self.menu = Menu(self, self.binding_source)
        self.editor = ImageEditor(self, self.resize_image)
        self.closer = CloseEditor(self, self.close_editor)

    def binding_data(self):
        # BINDING.
        self.binding_source = {
            "POSITION": {
                "ROTATE": ctk.DoubleVar(value=DEFAULT_ROTATE),
                "ZOOM": ctk.DoubleVar(value=DEFAULT_ZOOM),
                "FLIP": ctk.StringVar(value=FLIP_OPTIONS[0]),
            },
            "COLOUR": {
                "BRIGHTNESS": ctk.DoubleVar(value=DEFAULT_BRIGHTNESS),
                "GRAYSCALE": ctk.BooleanVar(value=DEFAULT_GRAYSCALE),
                "INVERT": ctk.BooleanVar(value=DEFAULT_INVERT),
                "VIBRANCE": ctk.DoubleVar(value=DEFAULT_VIBRANCE),
            },
            "EFFECT": {
                "BLUR": ctk.DoubleVar(value=DEFAULT_BLUR),
                "CONTRAST": ctk.IntVar(value=DEFUALT_CONTRAST),
                "EFFECT": ctk.StringVar(value=EFFECT_OPTIONS[0]),
            },
        }
        # TRACING.
        for data_source in self.binding_source.values():
            for binding_data in data_source.values():
                binding_data.trace(ctk.W, self.manipulate_image)

    def manipulate_image(self, *args):
        self.image = self.original.copy()
        # ROTATE.
        value = self.binding_source["POSITION"]["ROTATE"].get()
        if value != DEFAULT_ROTATE:
            self.image = self.image.rotate(value)
        # ZOOM.
        value = self.binding_source["POSITION"]["ZOOM"].get()
        if value != DEFAULT_ZOOM:
            self.image = ImageOps.crop(self.image, value)
        # FLIP.
        match self.binding_source["POSITION"]["FLIP"].get():
            case "NONE":
                pass
            case "X":
                self.image = ImageOps.mirror(self.image)
            case "Y":
                self.image = ImageOps.flip(self.image)
            case "BOTH":
                self.image = ImageOps.mirror(self.image)
                self.image = ImageOps.flip(self.image)
        # BRIGHTNESS.
        value = self.binding_source["COLOUR"]["BRIGHTNESS"].get()
        if value != DEFAULT_BRIGHTNESS:
            ENHANCER = ImageEnhance.Brightness(self.image)
            self.image = ENHANCER.enhance(value)
        # VIBRANCE.
        value = self.binding_source["COLOUR"]["VIBRANCE"].get()
        if value != DEFAULT_VIBRANCE:
            ENHANCER = ImageEnhance.Color(self.image)
            self.image = ENHANCER.enhance(value)
        # GRAYSCALE.
        if self.binding_source["COLOUR"]["GRAYSCALE"].get():
            self.image = ImageOps.grayscale(self.image)
        # INVERT.
        if self.binding_source["COLOUR"]["INVERT"].get():
            self.image = ImageOps.invert(self.image)
        # BLUR.
        value = self.binding_source["EFFECT"]["BLUR"].get()
        if value != DEFAULT_BLUR:
            self.image = self.image.filter(ImageFilter.GaussianBlur(value))
        # CONTRAST.
        value = self.binding_source["EFFECT"]["CONTRAST"].get()
        if value != DEFUALT_CONTRAST:
            self.image = self.image.filter(ImageFilter.UnsharpMask(value))
        # EFFECTS.
        match self.binding_source["EFFECT"]["EFFECT"].get():
            case "NONE":
                pass
            case "EMBOSS":
                self.image = self.image.filter(ImageFilter.EMBOSS)
            case "FIND EDGES":
                self.image = self.image.filter(ImageFilter.FIND_EDGES)
            case "CONTOUR":
                self.image = self.image.filter(ImageFilter.CONTOUR)
            case "EDGE ENHANCE":
                self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        # SHOW IMAGE.
        self.show_image()

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

    def close_editor(self):
        # HIDE THE IMAGE EDITOR.
        self.menu.grid_forget()
        self.editor.grid_forget()
        self.closer.place_forget()
        # OPEN THE IMAGE LOADER.
        self.loader = ImageLoader(self, self.load_image)


if __name__ == "__main__":
    App().mainloop()
