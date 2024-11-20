from pathlib import Path
import tkinter as tk
from tkinter import Canvas, PhotoImage

class InvoiceApp:
    def __init__(self, invoice_data):
        """Inisialisasi InvoiceApp dengan data."""
        self.invoice_data = invoice_data
        self.window = tk.Tk()
        self.window.geometry("1024x720")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)
        
        self.ASSETS_PATH = Path(r"E:\UTS_PEMKOM\build\assets\frame4")
        self.image_refs = []  # Menyimpan referensi gambar
        
        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """Setup elemen UI untuk Invoice."""
        # (Elemen UI tetap sama seperti sebelumnya)

        # Tambahkan daftar barang
        self.display_invoice_items()

        # Tambahkan total
        self.canvas.create_text(
            800.0, 600.0, anchor="nw",
            text=f"Total: Rp {self.invoice_data['total']:,.2f}",
            fill="#FFFFF2",
            font=("Poppins SemiBold", 24 * -1)
        )

    def display_invoice_items(self):
        """Tampilkan barang pada invoice."""
        y_start = 300  # Posisi Y awal
        for item in self.invoice_data["items"]:
            self.canvas.create_text(
                112.0, y_start, anchor="nw",
                text=item["nama"],
                fill="#000000",
                font=("Poppins", 14)
            )
            self.canvas.create_text(
                573.0, y_start, anchor="nw",
                text=str(item["jumlah"]),
                fill="#000000",
                font=("Poppins", 14)
            )
            self.canvas.create_text(
                768.0, y_start, anchor="nw",
                text=f"Rp {item['harga_satuan']:,.2f}",
                fill="#000000",
                font=("Poppins", 14)
            )
            y_start += 30  # Geser posisi Y ke bawah

    def run(self):
        """Menjalankan aplikasi."""
        self.window.mainloop()
