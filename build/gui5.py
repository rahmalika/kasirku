from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage


class InvoiceApp:
    def __init__(self):
        # Inisialisasi jendela utama
        self.window = Tk()
        self.window.geometry("1024x720")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        # Path untuk aset
        self.ASSETS_PATH = Path(r"E:\UTS_PEMKOM\build\assets\frame4")
        self.image_refs = []  # Menyimpan referensi gambar

        # Setup UI
        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        """Mengembalikan path relatif untuk file aset."""
        return self.ASSETS_PATH / Path(path)

    def setup_ui(self):
        """Menyusun elemen UI."""
        # Canvas
        self.canvas = Canvas(
            self.window,
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
            112.0, 41.0, anchor="nw",
            text="Invoice Belanja",
            fill="#FFFFF2",
            font=("Poppins ExtraBold", 48 * -1)
        )
        self.canvas.create_text(
            91.0, 203.0, anchor="nw",
            text="No Invoice",
            fill="#FFFFF2",
            font=("Poppins SemiBold", 24 * -1)
        )
        self.canvas.create_text(
            112.0, 261.0, anchor="nw",
            text="Nama Barang",
            fill="#FFFFF2",
            font=("Poppins SemiBold", 24 * -1)
        )
        self.canvas.create_text(
            573.0, 261.0, anchor="nw",
            text="Qty",
            fill="#FFFFF2",
            font=("Poppins SemiBold", 24 * -1)
        )
        self.canvas.create_text(
            768.0, 253.0, anchor="nw",
            text="Harga",
            fill="#FFFFF2",
            font=("Poppins SemiBold", 24 * -1)
        )

        # Tambahkan tombol
        self.create_button(440.0, 565.0, "button_1.png", 145.0, 47.0, self.on_button_1_click)
        self.create_button(626.0, 565.0, "button_2.png", 196.0, 47.0, self.on_button_2_click)
        self.create_button(228.0, 565.0, "button_3.png", 145.0, 47.0, self.on_button_3_click)

    def add_image(self, file_name, x, y):
        """Menambahkan gambar ke canvas."""
        image = PhotoImage(file=self.relative_to_assets(file_name))
        self.image_refs.append(image)  # Simpan referensi gambar
        self.canvas.create_image(x, y, image=image)

    def create_button(self, x, y, image_file, width, height, command):
        """Membuat tombol."""
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

    # Callback tombol
    def on_button_1_click(self):
        print("Button 1 clicked")

    def on_button_2_click(self):
        print("Button 2 clicked")

    def on_button_3_click(self):
        print("Button 3 clicked")

    def run(self):
        """Menjalankan aplikasi."""
        self.window.mainloop()


# Jalankan aplikasi
if __name__ == "__main__":
    app = InvoiceApp()
    app.run()
