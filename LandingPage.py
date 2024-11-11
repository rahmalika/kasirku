from tkinter import *
from AplikasiPenjual import AplikasiPenjual
from tkinter import messagebox  # Import messagebox secara eksplisit

class AplikasiKasirku:
    def __init__(self, window):
        self.window = window
        self.window.title("KasirKu")
        self.window.geometry("720x480")
        self.window.configure(bg="#FFF2DB")
        
        # Bind close event to on_closing function
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.UI_Model()

    def UI_Model(self):
        # Canvas utama
        self.canvas = Canvas(
            self.window,
            bg="#FFF2DB",
            height=480,
            width=720,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Judul utama
        self.canvas.create_text(
            360, 80, text="Selamat Datang di KasirKu", fill="#000000",
            font=("Poppins", 36, "bold"), anchor="center"
        )
        
        # Deskripsi teks
        self.canvas.create_text(
            360, 150, text="Pembayaran Mudah dalam Genggaman Anda!", fill="#000000",
            font=("Poppins", 14), anchor="center"
        )
        
        # Tombol Penjual
        self.tombol_penjual = Button(
            self.window, text="Penjual", font=("Arial", 14), bg="#3bdfff", fg="black",
            width=10, height=2, relief="flat", command=self.buka_halaman_penjual
        )
        self.tombol_penjual.place(relx=0.35, rely=0.6, anchor=CENTER)
        
        # Tombol Pembeli
        self.tombol_pembeli = Button(
            self.window, text="Pembeli", font=("Arial", 14), bg="#3bdfff", fg="black",
            width=10, height=2, relief="flat", command=self.buka_halaman_pembeli
        )
        self.tombol_pembeli.place(relx=0.65, rely=0.6, anchor=CENTER)
        
        # Footer dengan informasi hak cipta
        self.canvas.create_rectangle(
            0, 450, 720, 480, fill="#3bdfff", outline=""
        )
        self.canvas.create_text(
            360, 465, text="©2024 | Rahmaika Aumara Zilka 165231005", fill="black",
            font=("Arial", 10), anchor="center"
        )

    # Fungsi untuk membuka halaman Penjual
    def buka_halaman_penjual(self):
        AplikasiPenjual(self.window)

    # Fungsi untuk membuka halaman Pembeli
    def buka_halaman_pembeli(self):
        print("Halaman Penjual dibuka")  # Ganti dengan logika membuka halaman penjual

    # Fungsi untuk menangani peringatan saat menutup jendela
    def on_closing(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin menutup aplikasi?"):
            self.window.destroy()

if __name__ == "__main__":
    window = Tk()
    app = AplikasiKasirku(window)
    window.mainloop()
