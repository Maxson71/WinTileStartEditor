from customtkinter import *
from customtkinter import filedialog as fd
from PIL import Image

class WinTileStartEditor:
    def __init__(self):
        self.root = CTk()
        self.root.geometry("720x500")
        self.root.resizable(False, False)
        # configure grid layout (4x4)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure((2, 3), weight=0)
        self.root.grid_rowconfigure((0, 1, 2), weight=1)
        self.init()

    def init(self):
        self.root.title("WinTileStartEditor")
        self.root.iconbitmap("resources/icon.ico")

        self.root.bind("<Escape>", self.__close)

    def run(self):
        self.draw_widgets()

        self.root.mainloop()

    def draw_widgets(self):
        self.sidebar_frame = CTkFrame(self.root, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = CTkLabel(self.sidebar_frame, text="WinTileStartEditor",
                                                 font=CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.OpenImageButtom = CTkButton(self.sidebar_frame, text="Open", command=self.open_image)
        self.OpenImageButtom.grid(row=1, column=0, padx=10, pady=5)

        self.SaveImageButtom = CTkButton(self.sidebar_frame, text="Save", command=self.save_image)
        self.SaveImageButtom.grid(row=2, column=0, padx=10, pady=5)

        self.radius_label = CTkLabel(self.sidebar_frame, text="Radius: 25")
        self.radius_label.grid(row=3, column=0, padx=20, pady=5)

        self.radius_slider = CTkSlider(self.sidebar_frame, from_=0, to=50, number_of_steps=50, orientation="horizontal")
        self.radius_slider.grid(row=4, column=0, padx=20, pady=5)

        self.radius_slider.bind("<ButtonRelease-1>", self.update_radius_label)

        self.image_label = CTkLabel(self.root, image=None, text="")
        self.image_label.grid(row=0, column=1, rowspan=4, sticky="nsew")

    def update_radius_label(self, event=None):
        radius = self.radius_slider.get()
        self.radius_label.configure(text=f"Radius: {int(radius)}")

    def display_image(self):
        if hasattr(self, 'image'):
            radius = self.radius_slider.get()
            ctk_image = CTkImage(self.image, size=(450, 450))
            self.image_label.configure(image=ctk_image)
            self.image_label.image = ctk_image

    def open_image(self):
        image_path = fd.askopenfilenames(filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))
        if image_path:
            self.image = Image.open(image_path[0])
            self.display_image()

    def save_image(self):
        if self.image:
            save_path = fd.asksaveasfilename(defaultextension=".png", filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))
            if save_path:
                self.image.save(save_path)


    def __close(self, event):
        self.root.quit()

if __name__ == "__main__":
    WinTileStartEditor().run()
