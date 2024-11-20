from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage


class TambahBarangApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x720")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.ASSETS_PATH = Path(r"E:\\UTS_PEMKOM\\build\\assets\\frame3")
        self.image_refs = []  # List untuk menyimpan referensi gambar
        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def setup_ui(self):
        # Canvas setup
        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=720,
            width=1024,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Background images
        self.add_image("image_1.png", 512.0, 384.0)
        self.add_image("image_2.png", 512.0, 686.0)

        # Text elements
        self.canvas.create_text(
            112.0, 74.0, anchor="nw",
            text="Halaman Tambah Barang",
            fill="#FFFFF2",
            font=("Poppins ExtraBold", 48 * -1)
        )
        self.canvas.create_text(
            287.0, 176.0, anchor="nw",
            text="Silahkan data barang dengan nilai yang valid",
            fill="#FFFFF2",
            font=("Poppins SemiBold", 24 * -1)
        )

        # Input fields
        self.create_input_field(130.0, 261.0, "entry_1.png", 765.0, 55.0)
        self.create_input_field(129.0, 356.0, "entry_2.png", 765.0, 55.0)
        self.create_input_field(131.0, 451.0, "entry_3.png", 765.0, 55.0)

        # Buttons
        self.create_button(116.0, 556.0, "button_1.png", 145.0, 47.0, self.on_button_1_click)
        self.create_button(767.0, 546.0, "button_2.png", 145.0, 47.0, self.on_button_2_click)

    def add_image(self, file_name, x, y):
        image = PhotoImage(file=self.relative_to_assets(file_name))
        self.image_refs.append(image)  # Simpan referensi gambar
        self.canvas.create_image(x, y, image=image)

    def create_input_field(self, x, y, image_file, width, height):
        entry_image = PhotoImage(file=self.relative_to_assets(image_file))
        self.image_refs.append(entry_image)  # Simpan referensi gambar
        self.canvas.create_image(x + width / 2, y + height / 2, image=entry_image)
        entry = Text(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        entry.place(x=x, y=y, width=width, height=height)
        setattr(self, f"{image_file}_entry", entry)

    def create_button(self, x, y, image_file, width, height, command):
        button_image = PhotoImage(file=self.relative_to_assets(image_file))
        self.image_refs.append(button_image)  # Simpan referensi gambar
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        button.place(x=x, y=y, width=width, height=height)
        setattr(self, f"{image_file}_button", button)

    def on_button_1_click(self):
        print("Button 1 clicked")

    def on_button_2_click(self):
        print("Button 2 clicked")


if __name__ == "__main__":
    root = Tk()
    app = TambahBarangApp(root)
    root.mainloop()
