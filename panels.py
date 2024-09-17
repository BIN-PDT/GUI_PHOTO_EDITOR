import customtkinter as ctk
from settings import *


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=DARK_GREY)
        self.pack(fill=ctk.X, padx=8, pady=4)


class SliderPanel(Panel):
    def __init__(self, parent, label, minimum, maximum, binding_data):
        super().__init__(parent)
        # LAYOUT.
        self.rowconfigure((0, 1), weight=1, uniform="B")
        self.columnconfigure((0, 1), weight=1, uniform="B")
        # DATA.
        self.binding_data = binding_data
        font = ctk.CTkFont(MAIN_FONT, 14)
        # WIDGETS.
        ctk.CTkLabel(master=self, text=label, font=font).grid(
            column=0, row=0, sticky=ctk.W, padx=10
        )

        self.output = ctk.CTkLabel(master=self, text=binding_data.get(), font=font)
        self.output.grid(column=1, row=0, sticky=ctk.E, padx=10)

        ctk.CTkSlider(
            master=self,
            from_=minimum,
            to=maximum,
            fg_color=SLIDER_BG,
            variable=binding_data,
            command=self.update_output,
        ).grid(column=0, row=1, columnspan=2, sticky=ctk.EW, padx=5, pady=5)

    def update_output(self, *args):
        self.output.configure(text=f"{self.binding_data.get():.1f}")


class SegmentPanel(Panel):
    def __init__(self, parent, label, options, binding_data):
        super().__init__(parent)
        # DATA.
        font = ctk.CTkFont(MAIN_FONT, 14, "normal")
        # WIDGETS
        ctk.CTkLabel(master=self, text=label, font=font).pack()

        ctk.CTkSegmentedButton(
            master=self, values=options, font=font, variable=binding_data
        ).pack(expand=ctk.TRUE, fill=ctk.BOTH, padx=5, pady=5)


class SwitchPanel(Panel):
    def __init__(self, parent, *switches):
        super().__init__(parent)
        # WIDGET.
        for text, data_binding in switches:
            ctk.CTkSwitch(
                master=self,
                text=text,
                font=ctk.CTkFont(MAIN_FONT, 14),
                fg_color=SLIDER_BG,
                button_color=BLUE,
                variable=data_binding,
            ).pack(side=ctk.LEFT, expand=ctk.TRUE, fill=ctk.BOTH, padx=10, pady=5)


class DropDownPanel(ctk.CTkOptionMenu):
    def __init__(self, parent, options, data_binding):
        font = ctk.CTkFont(MAIN_FONT, 14)
        super().__init__(
            master=parent,
            height=32,
            values=options,
            font=font,
            dropdown_font=font,
            fg_color=DARK_GREY,
            button_color=DROPDOWN_MAIN,
            dropdown_fg_color=DROPDOWN_MENU,
            button_hover_color=DROPDOWN_HOVER,
            variable=data_binding,
        )
        self.pack(fill=ctk.X, padx=8, pady=4)
