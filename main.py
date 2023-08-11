import numpy as np
from PIL import Image, ImageDraw, ImageFont
from customtkinter import *
from customtkinter import filedialog as fd
from CTkColorPicker import *


class WinTileStartEditor:
    def __init__(self):
        self.root = CTk()
        self.root.geometry("740x500")
        self.root.minsize(740,500)

        self.glow_color = (255, 255, 255)
        self.image = None

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, minsize=220)
        self.root.grid_rowconfigure(0, weight=1)

        self.init()

    def init(self):
        self.root.title("WinTileStartEditor")
        self.root.iconbitmap("resources/icon.ico")

    def run(self):
        self.draw_widgets()

        self.root.mainloop()

    def draw_widgets(self):

        self.sidebar_frame = CTkFrame(self.root, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10)

        self.logo_label = CTkLabel(self.sidebar_frame, text="WinTileStartEditor",
                                                 font=CTkFont("<Biennale>", size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.style_segmented_button = CTkSegmentedButton(self.sidebar_frame, command=self.segmented_button_event)
        self.style_segmented_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.style_segmented_button.configure(values=["Win10", "Win11"])
        self.style_segmented_button.set("Win10")

        self.button_frame = CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, padx=10, pady=5)

        self.open_image_buttom = CTkButton(self.button_frame, text="Open", command=self.open_image, width = 80)
        self.open_image_buttom.grid(row=0, column=0, padx=10, pady=5)

        self.save_image_buttom = CTkButton(self.button_frame, text="Save", command=self.save_image, width = 80)
        self.save_image_buttom.grid(row=0, column=1, padx=10, pady=5)

        self.radius_label = CTkLabel(self.sidebar_frame, text="Radius: 0")
        self.radius_label.grid(row=3, column=0, padx=20, pady=1)

        self.radius_slider = CTkSlider(self.sidebar_frame, from_=0, to=100, border_width=3 , command=self.slider_radius_event)
        self.radius_slider.set(0)
        self.radius_slider.grid(row=4, column=0, padx=20, pady=5)

        self.text_entry = CTkEntry(self.sidebar_frame, height=30)
        self.text_entry.grid(row=5, column=0, padx=20, pady=5, sticky="nsew")
        self.text_entry.bind("<KeyRelease>", self.text_changed)

        self.size_text_label = CTkLabel(self.sidebar_frame, text="Size text: 150")
        self.size_text_label.grid(row=6, column=0, padx=10, pady=1)

        self.size_text_slider = CTkSlider(self.sidebar_frame, from_=50, to=250, border_width=3, command=self.slider_size_text_event)
        self.size_text_slider.set(150)
        self.size_text_slider.grid(row=7, column=0, padx=20, pady=1)

        self.double_text_var = IntVar(value=0)
        self.double_text_check = CTkCheckBox(self.sidebar_frame, text="Double text",
                                      variable=self.double_text_var, onvalue=1, offvalue=0, checkbox_width = 20, checkbox_height = 20)
        self.double_text_check.grid(row=8, column=0, padx=10, pady=10)

        self.choose_glow_color_frame = CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.choose_glow_color_frame.grid(row=9, column=0, padx=10, pady=5)

        self.check_glow_var = BooleanVar(value=False)
        self.choose_glow_color_check = CTkCheckBox(self.choose_glow_color_frame, text="Add glow", command=self.glow_check_changed,
                                                   variable=self.check_glow_var, onvalue=True, offvalue=False,
                                                   checkbox_width = 20, checkbox_height = 20)
        self.choose_glow_color_check.grid(row=0, column=0, padx=10, pady=5)

        self.choose_glow_color_button = CTkButton(self.choose_glow_color_frame, text="", fg_color="white",hover_color="white",
                                                  command=self.ask_color, state="disabled", width = 30, height = 30)
        self.choose_glow_color_button.grid(row=0, column=1, padx=10, pady=5)

        self.image_label = CTkLabel(self.root, image=self.image, text="")
        self.image_label.grid(row=0, column=1, rowspan=4, sticky="nsew")

    def glow_check_changed(self):
        if self.check_glow_var.get():
            self.choose_glow_color_button.configure(state="normal")
        else:
            self.choose_glow_color_button.configure(state="disabled")
        if self.image is not None:
            self.create_grow_rounded_image()

    def ask_color(self):
        pick_color = AskColor()
        color = pick_color.get()
        if color is not None:
            self.glow_color_changed(color)
            self.choose_glow_color_button.configure(fg_color=color)

    def glow_color_changed(self, color):
        self.glow_color = tuple(int(color.replace("#", "", 1)[i:i + 2], 16) for i in (0, 2, 4))
        if self.image is not None:
            self.create_grow_rounded_image()

    def text_changed(self, event):
        if self.image is not None:
            self.create_text_rounded_image()

    def segmented_button_event(self, value):
        if value == "Win10":
            self.radius_slider.set(0)
            self.slider_radius_event(0)
        else:
            self.radius_slider.set(50)
            self.slider_radius_event(50)

    def slider_size_text_event(self, value):
        self.size_text_label.configure(text=f"Size text: {int(value)}")
        if self.image is not None:
            self.create_text_rounded_image()

    def slider_radius_event(self, value):
        self.radius_label.configure(text=f"Radius: {int(value)}")
        if self.image is not None:
            self.create_final_rounded_image()

    def create_rounded_image(self):
        width, height = self.image.size
        self.rounded_image = Image.new('RGBA', (width, height))
        self.rounded_image.paste(self.image, (0, 0), self.image)

        self.create_grow_rounded_image()

    def create_grow_rounded_image(self):
        width, height = self.image.size
        self.grow_rounded_image = Image.new('RGBA', (width, height))
        self.grow_rounded_image.paste(self.rounded_image, (0, 0))
        if self.check_glow_var.get():
            glow_image = Image.open("resources/glow/glow_1.png").convert("RGBA").resize((width, height))
            glow_image = self.change_glow_color(glow_image)
            self.grow_rounded_image.paste(glow_image, (0, 0), glow_image)

        self.create_text_rounded_image()

    def change_glow_color(self, image):
        data = np.array(image)
        color = self.glow_color
        red, green, blue, alpha = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
        red[color != 0] = color[0]
        green[color != 0] = color[1]
        blue[color != 0] = color[2]
        return Image.fromarray(np.stack((red, green, blue, alpha), axis=-1), 'RGBA')

    def create_text_rounded_image(self):
        width, height = self.image.size
        size_text = int(self.size_text_slider.get())

        self.text_rounded_image = Image.new('RGBA', (width, height))
        self.text_rounded_image.paste(self.grow_rounded_image, (0, 0), self.grow_rounded_image)

        rounded_image_with_text = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(rounded_image_with_text)
        text = self.text_entry.get()

        font = ImageFont.truetype("resources/fonts/BiennaleBold.otf", size=size_text)
        draw.text((50, height - 60), text, font=font, fill=(255, 255, 255, 255), anchor="ls")
        self.text_rounded_image.paste(rounded_image_with_text, (0, 0), rounded_image_with_text)

        self.create_icon_rounded_image()

    def create_icon_rounded_image(self):
        width, height = self.image.size
        self.icon_rounded_image = Image.new('RGBA', (width, height))
        self.icon_rounded_image.paste(self.text_rounded_image, (0, 0), self.text_rounded_image)
        glow2_image = Image.open("resources/glow/glow_2.png").resize((width, height))
        self.icon_rounded_image.paste(self.text_rounded_image, (0, 0), self.text_rounded_image)
        self.icon_rounded_image.paste(glow2_image, (0, 0), glow2_image)

        self.create_final_rounded_image()


    def create_final_rounded_image(self):
            width, height = self.image.size
            mask = self.create_mask()
            self.rounded_image_final = Image.new('RGBA', (width, height))
            self.rounded_image_final.paste(self.icon_rounded_image, mask=mask)

            self.display_image()

    def create_mask(self):
        radius = int(self.radius_slider.get())
        width, height = self.image.size
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)

        draw.rectangle((0, radius, width, height - radius), fill=255)
        draw.rectangle((radius, 0, width - radius, height), fill=255)

        draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
        draw.ellipse((0, height - (radius * 2) - 1, (radius * 2), height - 1), fill=255)
        draw.ellipse((width - (radius * 2) - 1, 0, width - 1, (radius * 2)), fill=255)
        draw.ellipse((width - (radius * 2) - 1, height - (radius * 2) - 1, width - 1, height - 1), fill=255)

        return mask

    def display_image(self):
        ctk_image = self.convert_to_ctk_image(self.rounded_image_final)
        self.image_label.configure(image=ctk_image)
        self.image_label.image = ctk_image

    def convert_to_ctk_image(self, pil_image):

        width, height = self.image.size
        if width >= height:
            ctk_image = CTkImage(pil_image, size=(450, 450//(width/height)))
        else:
            ctk_image = CTkImage(pil_image, size=(450//(height/width), 450))
        return ctk_image

    def open_image(self):
        image_path = fd.askopenfilenames(filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))
        if image_path:
            self.image = Image.open(image_path[0])
            if self.image is not None:
                self.create_rounded_image()

    def save_image(self):
        if self.image is not None:
            save_path = fd.asksaveasfilename(defaultextension=".png", filetypes=(("Images", "*.png"),))
            if save_path:
                self.rounded_image_final.save(save_path, format="PNG")

    def __close(self, event):
        self.root.quit()

if __name__ == "__main__":
    WinTileStartEditor().run()
