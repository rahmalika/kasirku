from pathlib import Path # membantu mengetahui keberadaan file(lokasinya)
from tkinter import Tk, Canvas, Button, PhotoImage
from gui_login import LoginApp # ini halaman login
from gui_pelanggan import PelangganApp # ini halaman pelanggan

class KasirApp: # ini halaman utama
    def __init__(self, root): # menginisialisasiroot adalah halaman utama kita
        self.root = root
        self.root.geometry("1024x720")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        # Define paths
        self.output_path = Path(__file__).parent # naih ini membantu mengetahui lokasi file
        self.assets_path = self.output_path / Path(r"E:\UTS_PEMKOM\build\assets\frame0")

        # Create canvas
        self.canvas = Canvas( # ini kita membuat canvas
            root,
            bg="#FFFFFF",
            height=720,
            width=1024,
            bd=0,
            highlightthickness=0,
            relief="ridge" # ini untuk membuat border
        )
        self.canvas.place(x=0, y=0) # ini untuk memposisikan canvas

        # Load assets
        self.setup_assets() # nah ini untuk memanggil fungsi setup_assets

        # Create UI components
        self.setup_ui() # nah ini untuk memanggil fungsi setup_ui

    def relative_to_assets(self, path: str) -> Path: # ini fungsi untuk mengetahui keberadaan file
        return self.assets_path / Path(path)

    def setup_assets(self): # ini fungsi untuk memanggil file
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))

    def setup_ui(self): # ini fungsi untuk membuat UI
        # Background image
        self.canvas.create_image( # ini untuk membuat gambar
            512.0,
            384.0,
            image=self.image_1
        )

        # Welcome text
        self.canvas.create_text( # ini untuk membuat teks
            143.0,
            75.0,
            anchor="nw",
            text="SELAMAT DATANG DI KASIRKU",
            fill="#FFFFF2",
            font=("Poppins ExtraBold", 48 * -1)
        )

        # Subtitle text
        self.canvas.create_text( # ini untuk membuat teks
            290.0,
            191.0,
            anchor="nw",
            text="Pembayaran Mudah dalam Genggaman Anda!",
            fill="#FFFFF2",
            font=("Poppins SemiBold", 24 * -1)
        )

        # Footer image
        self.canvas.create_image( # ini untuk membuat gambar
            512.0,
            686.0,
            image=self.image_2
        )

        # Buttons
        self.button_1 = Button( # ini untuk membuat tombol
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_1_click,
            relief="flat"
        )
        self.button_1.place( # ini untuk memposisikan tombol
            x=287.0,
            y=354.0,
            width=454.0,
            height=78.0
        )

        self.button_2 = Button( # ini untuk membuat tombol
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_2_click,
            relief="flat"
        )
        self.button_2.place( # ini untuk memposisikan tombol
            x=285.0,
            y=483.0,
            width=454.0,
            height=78.0
        )

    def on_button_1_click(self): # ini fungsi untuk membuat tombol
        LoginApp(self.root)

    def on_button_2_click(self): # ini fungsi untuk membuat tombol
        print("Button 2 clicked") # ini untuk menampilkan pesan
        PelangganApp(self.root)    # ini untuk memanggil class PelangganApp

if __name__ == "__main__": # ini fungsi utama
    root = Tk() # ini untuk membuat halaman utama kita
    app = KasirApp(root) # ini untuk memanggil class KasirApp
    root.mainloop() # ini untuk menjalankan aplikasi
