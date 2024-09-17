import customtkinter as ctk
from settings import *


class ImageLoader(ctk.CTkFrame):
    def __init__(self, parent, load_image):
        super().__init__(master=parent, fg_color=BLACK)
        self.grid(column=0, row=0, columnspan=2, sticky=ctk.NSEW)
        # DATA.
        self.load_image = load_image
        # WIDGET.
        ctk.CTkButton(
            master=self,
            height=50,
            text="Open Image",
            font=ctk.CTkFont("Cambria", 20, "bold", "italic"),
            command=self.open_dialog,
        ).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def open_dialog(self):
        path = ctk.filedialog.askopenfilename(
            title="Select an image file",
            filetypes=[("Image", "*.png *.jpg *.jpeg")],
        )
        self.load_image(path)
