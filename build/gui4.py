from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage


class PelangganApp:
    def __init__(self):
        # Inisialisasi aplikasi
        self.root = Tk()
        self.root.geometry("1024x720")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.ASSETS_PATH = Path(r"E:\UTS_PEMKOM\build\assets\frame4")
        self.image_refs = []  # Menyimpan referensi gambar untuk mencegah penghapusan oleh garbage collector

        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        """Mendapatkan path relatif untuk file aset."""
        return self.ASSETS_PATH / Path(path)

    def setup_ui(self):
        """Menyusun elemen-elemen UI."""
        # Canvas
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

        # Tambahkan gambar latar belakang
        self.add_image("image_1.png", 512.0, 384.0)
        self.add_image("image_2.png", 512.0, 686.0)

        # Tambahkan teks
        self.canvas.create_text(
            144.0, 40.0, anchor="nw",
            text="Hallo, Pelanggan yang baik!",
            fill="#FFFFF2",
            font=("Poppins ExtraBold", 48 * -1)
        )
        self.canvas.create_text(
            286.0, 144.0, anchor="nw",
            text="silahkan masukkan kode barang dan jumlah yang kamu beli",
            fill="#FFFFF2",
            font=("Poppins SemiBold", 24 * -1)
        )

        # Tambahkan field input
        self.entry_1 = self.create_input_field(106.0, 243.0, "entry_1.png", 256.6352844238281, 33.0)
        self.entry_2 = self.create_input_field(373.0, 243.0, "entry_2.png", 152.0, 33.0)

        # Tambahkan tombol
        self.create_button(116.0, 556.0, "button_1.png", 145.0, 47.0, self.on_button_1_click)
        self.create_button(325.0, 556.0, "button_4.png", 145.0, 47.0, self.on_button_4_click)
        self.create_button(525.0, 556.0, "button_2.png", 145.0, 47.0, self.on_button_2_click)
        self.create_button(748.0, 556.0, "button_3.png", 145.0, 47.0, self.on_button_3_click)

        # Rectangle putih
        self.canvas.create_rectangle(
            100.0,
            305.0,
            963.6318969726562,
            527.0,
            fill="#FFFFFF",
            outline=""
        )

    def add_image(self, file_name, x, y):
        """Menambahkan gambar ke canvas."""
        image = PhotoImage(file=self.relative_to_assets(file_name))
        self.image_refs.append(image)  # Menyimpan referensi gambar
        self.canvas.create_image(x, y, image=image)

    def create_input_field(self, x, y, image_file, width, height):
        """Membuat field input."""
        entry_image = PhotoImage(file=self.relative_to_assets(image_file))
        self.image_refs.append(entry_image)  # Menyimpan referensi gambar
        self.canvas.create_image(x + width / 2, y + height / 2, image=entry_image)
        entry = Text(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        entry.place(x=x, y=y, width=width, height=height)
        return entry

    def create_button(self, x, y, image_file, width, height, command):
        """Membuat tombol."""
        button_image = PhotoImage(file=self.relative_to_assets(image_file))
        self.image_refs.append(button_image)  # Menyimpan referensi gambar
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        button.place(x=x, y=y, width=width, height=height)

    # Callback tombol
    def on_button_1_click(self):
        print("Button 1 clicked")

    def on_button_2_click(self):
        print("Button 2 clicked")

    def on_button_3_click(self):
        print("Button 3 clicked")

    def on_button_4_click(self):
        print("Button 4 clicked")

    def run(self):
        """Menjalankan aplikasi."""
        self.root.mainloop()


# Jalankan aplikasi
if __name__ == "__main__":
    app = PelangganApp()
    app.run()
