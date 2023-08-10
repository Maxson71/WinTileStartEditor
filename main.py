from PIL import Image, ImageDraw, ImageFont
from customtkinter import *
from customtkinter import filedialog as fd


class WinTileStartEditor:
    def __init__(self):
        self.root = CTk()
        self.root.geometry("740x500")
        self.root.minsize(740,500)
        self.image = None
        self.root.grid_columnconfigure(1, weight=1)
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
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))

        self.button_frame = CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, padx=20, pady=10)

        self.open_image_buttom = CTkButton(self.button_frame, text="Open", command=self.open_image, width = 80)
        self.open_image_buttom.grid(row=0, column=0, padx=10, pady=5)

        self.save_image_buttom = CTkButton(self.button_frame, text="Save", command=self.save_image, width = 80)
        self.save_image_buttom.grid(row=0, column=1, padx=10, pady=5)

        self.style_segmented_button = CTkSegmentedButton(self.sidebar_frame, command=self.segmented_button_event)
        self.style_segmented_button.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.style_segmented_button.configure(values=["Win10", "Win11"])
        self.style_segmented_button.set("Win10")

        self.radius_label = CTkLabel(self.sidebar_frame, text="Radius: 0")
        self.radius_label.grid(row=3, column=0, padx=20, pady=5)

        self.radius_slider = CTkSlider(self.sidebar_frame, from_=0, to=100, command=self.slider_event)
        self.radius_slider.set(0)
        self.radius_slider.grid(row=4, column=0, padx=20, pady=5)

        self.image_label = CTkLabel(self.root, image=self.image, text="")
        self.image_label.grid(row=0, column=1, rowspan=4, sticky="nsew")

    def segmented_button_event(self, value):
        if value == "Win10":
            self.radius_slider.set(0)
            self.slider_event(0)
        else:
            self.radius_slider.set(50)
            self.slider_event(50)

    def slider_event(self, value):
        self.radius_label.configure(text=f"Radius: {int(value)}")
        self.display_image()

    def display_image(self):
        if hasattr(self, 'image'):
            if self.image is not None:
                radius = int(self.radius_slider.get())

                width, height = self.image.size

                mask = Image.new('L', (width, height), 0)
                draw = ImageDraw.Draw(mask)
                draw.rectangle((0, radius, width, height - radius), fill=255)
                draw.rectangle((radius, 0, width - radius, height), fill=255)

                draw.ellipse((0, 0, radius*2, radius*2), fill=255)
                draw.ellipse((0, height - (radius*2)-1, (radius*2), height-1), fill=255)
                draw.ellipse((width - (radius*2)-1, 0, width-1, (radius*2)), fill=255)
                draw.ellipse((width - (radius*2)-1, height - (radius*2)-1, width-1, height-1), fill=255)

                # Застосувати маску на зображення
                self.rounded_image = Image.new('RGBA', (width, height))
                self.rounded_image.paste(self.image, mask=mask)

                # Відобразити зображення на етикетці
                ctk_image = self.convert_to_ctk_image(self.rounded_image)
                self.image_label.configure(image=ctk_image)
                self.image_label.image = ctk_image

    def convert_to_ctk_image(self, pil_image):
        ctk_image = CTkImage(pil_image, size=(450, 450))
        return ctk_image

    def open_image(self):
        image_path = fd.askopenfilenames(filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))
        if image_path:
            self.image = Image.open(image_path[0])
            self.display_image()

    def save_image(self):
        if self.image is not None:
            save_path = fd.asksaveasfilename(defaultextension=".png", filetypes=(("Images", "*.png"),))
            if save_path:
                self.rounded_image.save(save_path, format="PNG")



    def __close(self, event):
        self.root.quit()

if __name__ == "__main__":
    WinTileStartEditor().run()
