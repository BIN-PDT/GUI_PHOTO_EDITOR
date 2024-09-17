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


class ResetButton(ctk.CTkButton):
    def __init__(self, parent, *data_bindings):
        super().__init__(
            master=parent,
            height=32,
            text="RESET",
            font=ctk.CTkFont(MAIN_FONT, 14),
            command=lambda: self.update_data(data_bindings),
        )
        self.pack(side=ctk.BOTTOM, pady=10)

    def update_data(self, data_bindings):
        for data_binding in data_bindings:
            data_binding[0].set(data_binding[1])


class FileNamePanel(Panel):
    def __init__(self, parent, binding_file_name, binding_extension):
        super().__init__(parent)
        # DATA.
        self.binding_file_name = binding_file_name
        self.binding_extension = binding_extension
        self.binding_file_name.trace_add("write", self.update_output)
        self.binding_extension.trace_add("write", self.update_output)
        font_main = ctk.CTkFont(MAIN_FONT, 14)
        font_path = ctk.CTkFont(PATH_FONT, 14)
        # WIDGETS.
        ctk.CTkEntry(
            master=self,
            height=36,
            font=font_path,
            justify=ctk.CENTER,
            textvariable=self.binding_file_name,
        ).pack(fill=ctk.X, padx=20, pady=10)

        extension_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkRadioButton(
            master=extension_frame,
            value="png",
            text="PNG",
            font=font_main,
            radiobutton_width=10,
            radiobutton_height=10,
            border_width_checked=2,
            border_width_unchecked=2,
            variable=self.binding_extension,
        ).pack(side=ctk.LEFT, expand=ctk.TRUE, fill=ctk.X)

        ctk.CTkRadioButton(
            master=extension_frame,
            value="jpg",
            text="JPG",
            font=font_main,
            radiobutton_width=10,
            radiobutton_height=10,
            border_width_checked=2,
            border_width_unchecked=2,
            variable=self.binding_extension,
        ).pack(side=ctk.LEFT, expand=ctk.TRUE, fill=ctk.X)
        extension_frame.pack(expand=ctk.TRUE, fill=ctk.X, padx=20, pady=5)

        self.output = ctk.CTkLabel(master=self, height=36, font=font_path)
        self.output.pack(padx=20, pady=5)
        # FIRST PROCESS.
        self.update_output()

    def update_output(self, *args):
        if file_name := self.binding_file_name.get():
            full_path = f"{file_name.replace(' ', '_')}.{self.binding_extension.get()}"
            self.output.configure(text=full_path)
        else:
            self.output.configure(text="")


class FilePathPanel(Panel):
    def __init__(self, parent, binding_file_path):
        super().__init__(parent)
        # DATA.
        self.binding_file_path = binding_file_path
        # WIDGETS.
        ctk.CTkButton(
            master=self,
            text="OPEN EXPLORER",
            font=ctk.CTkFont(MAIN_FONT, 14),
            command=self.open_dialog,
        ).pack(padx=20, pady=10)

        self.output = ctk.CTkEntry(
            master=self,
            height=36,
            font=ctk.CTkFont(PATH_FONT, 14),
            justify=ctk.CENTER,
            textvariable=self.binding_file_path,
        )
        self.output.pack(expand=ctk.TRUE, fill=ctk.X, padx=20, pady=10)

    def open_dialog(self):
        self.binding_file_path.set(ctk.filedialog.askdirectory())


class SaveButton(ctk.CTkButton):
    def __init__(
        self,
        parent,
        binding_file_path,
        binding_file_name,
        binding_extension,
        save_image,
    ):
        super().__init__(
            master=parent,
            height=32,
            text="SAVE",
            font=ctk.CTkFont(MAIN_FONT, 14),
            command=self.download,
        )
        self.pack(side=ctk.BOTTOM, pady=10)
        # DATA.
        self.binding_file_path = binding_file_path
        self.binding_file_name = binding_file_name
        self.binding_extension = binding_extension
        self.save_image = save_image

    def download(self):
        self.save_image(
            self.binding_file_path.get(),
            self.binding_file_name.get(),
            self.binding_extension.get(),
        )
