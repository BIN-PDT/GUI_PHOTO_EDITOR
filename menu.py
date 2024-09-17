import customtkinter as ctk
from panels import *


class Menu(ctk.CTkTabview):
    def __init__(self, parent, binding_source):
        super().__init__(master=parent)
        self.grid(column=0, row=0, sticky=ctk.NSEW, padx=10, pady=10)
        # TABS.
        self.add("POSITION")
        self.add("COLOUR")
        self.add("EFFECT")
        self.add("EXPORT")
        # FRAMES.
        PositionFrame(self.tab("POSITION"), binding_source["POSITION"])
        ColourFrame(self.tab("COLOUR"))
        EffectFrame(self.tab("EFFECT"))
        ExportFrame(self.tab("EXPORT"))


class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent, data_source):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=ctk.TRUE, fill=ctk.BOTH)
        # WIDGETS.
        SliderPanel(self, "ROTATION", 0, 360, data_source["ROTATE"])
        SliderPanel(self, "ZOOM", 0, 200, data_source["ZOOM"])
        SegmentPanel(self, "FLIP", FLIP_OPTIONS, data_source["FLIP"])


class ColourFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=ctk.TRUE, fill=ctk.BOTH)


class EffectFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=ctk.TRUE, fill=ctk.BOTH)


class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=ctk.TRUE, fill=ctk.BOTH)
