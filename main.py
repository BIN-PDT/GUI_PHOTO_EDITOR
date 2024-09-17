import customtkinter as ctk
from os.path import join, exists
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
        try:
            self.original = Image.open(path)
        except:
            pass
        else:
            self.image = self.original.copy()
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_ratio = self.image.width / self.image.height
            # HIDE THE IMAGE LOADER.
            self.loader.grid_forget()
            # OPEN THE IMAGE EDITOR.
            self.editor = ImageEditor(self, self.resize_image)
            self.menu = Menu(self, self.binding_source, path, self.save_image)
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
                "SHARPNESS": ctk.DoubleVar(value=DEFAULT_SHARPNESS),
                "CONTRAST": ctk.DoubleVar(value=DEFAULT_COLOR_CONTRAST),
            },
            "EFFECT": {
                "BLUR": ctk.DoubleVar(value=DEFAULT_BLUR),
                "CONTRAST": ctk.IntVar(value=DEFAULT_EFFECT_CONTRAST),
                "EFFECT": ctk.StringVar(value=EFFECT_OPTIONS[0]),
            },
        }
        # TRACING.
        for data_source in self.binding_source.values():
            for binding_data in data_source.values():
                binding_data.trace_add("write", self.manipulate_image)

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
        # SHARPNESS.
        value = self.binding_source["COLOUR"]["SHARPNESS"].get()
        if value != DEFAULT_SHARPNESS:
            ENHANCER = ImageEnhance.Sharpness(self.image)
            self.image = ENHANCER.enhance(value)
        # COLOR CONTRAST.
        value = self.binding_source["COLOUR"]["CONTRAST"].get()
        if value != DEFAULT_COLOR_CONTRAST:
            ENHANCER = ImageEnhance.Contrast(self.image)
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
        # EFFECT CONTRAST.
        value = self.binding_source["EFFECT"]["CONTRAST"].get()
        if value != DEFAULT_EFFECT_CONTRAST:
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
            case "BLUR":
                self.image = self.image.filter(ImageFilter.BLUR)
            case "DETAIL":
                self.image = self.image.filter(ImageFilter.DETAIL)
            case "SHARPEN":
                self.image = self.image.filter(ImageFilter.SHARPEN)
            case "SMOOTH":
                self.image = self.image.filter(ImageFilter.SMOOTH_MORE)
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

    def save_image(self, file_path, file_name, extension):
        # HANDLE NO FILE NAME.
        file_name = file_name if file_name else "default"
        path = f"{join(file_path, file_name)}.{extension}"
        # HANDLE EXISTED FILE.
        counter = 0
        while exists(path):
            counter += 1
            path = f"{join(file_path, file_name)}_{counter}.{extension}"
        # EXPORT IMAGE.
        self.image.save(path)


if __name__ == "__main__":
    App().mainloop()
