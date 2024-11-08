from tkinter import *
from tkinter import ttk  # Import ttk untuk Treeview
import csv

class AplikasiPenjual:
    def __init__(self, window):
        self.window = window
        self.window.title("KasirKu - Data Barang")
        self.window.geometry("800x600")
        self.window.configure(bg="#FFF2DB")
        
        # Setup UI
        self.UI_Model()

    def UI_Model(self):
        # Canvas utama
        self.canvas = Canvas(
            self.window,
            bg="#FFF2DB",
            height=600,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Judul utama
        self.canvas.create_rectangle(
            0, 0, 800, 120, fill="#23C9FF", outline=""
        )
        self.canvas.create_text(
            400, 60, text="Data Barang", fill="white",
            font=("Poppins", 36, "bold"), anchor="center"
        )

        # Treeview untuk menampilkan tabel data barang
        columns = ("kode", "nama", "stok", "harga")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=10)
        self.tree.heading("kode", text="Kode Barang")
        self.tree.heading("nama", text="Nama Barang")
        self.tree.heading("stok", text="Stock")
        self.tree.heading("harga", text="Harga")
        self.tree.column("kode", width=100, anchor=CENTER)
        self.tree.column("nama", width=200, anchor=CENTER)
        self.tree.column("stok", width=100, anchor=CENTER)
        self.tree.column("harga", width=150, anchor=CENTER)
        self.tree.place(relx=0.5, rely=0.4, anchor=CENTER)

        # Memuat data dari file CSV
        self.load_data_csv()

        # Tombol Edit
        self.tombol_edit = Button(
            self.window, text="Edit", font=("Arial", 12), bg="#3bdfff", fg="black",
            width=10, height=2, relief="flat", command=self.edit_data
        )
        self.tombol_edit.place(relx=0.2, rely=0.8, anchor=CENTER)

        # Tombol Tambah
        self.tombol_tambah = Button(
            self.window, text="Tambah", font=("Arial", 12), bg="#3bdfff", fg="black",
            width=10, height=2, relief="flat", command=self.tambah_data
        )
        self.tombol_tambah.place(relx=0.5, rely=0.8, anchor=CENTER)

        # Tombol Hapus
        self.tombol_hapus = Button(
            self.window, text="Hapus", font=("Arial", 12), bg="red", fg="white",
            width=10, height=2, relief="flat", command=self.hapus_data
        )
        self.tombol_hapus.place(relx=0.8, rely=0.8, anchor=CENTER)

        # Tombol Kembali
        self.tombol_kembali = Button(
            self.window, text="Kembali", font=("Arial", 12), bg="#3bdfff", fg="black",
            width=10, height=2, relief="flat", command=self.kembali
        )
        self.tombol_kembali.place(relx=0.5, rely=0.9, anchor=CENTER)

    def load_data_csv(self):
        try:
            with open("data_barang.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) == 4:  # Pastikan setiap baris memiliki 4 kolom
                        self.tree.insert("", "end", values=row)
        except FileNotFoundError:
            print("File data_barang.csv tidak ditemukan.")

    def edit_data(self):
        print("Edit data")

    def tambah_data(self):
        print("Tambah data")

    def hapus_data(self):
        selected_item = self.tree.selection()  # Mendapatkan item yang dipilih
        if selected_item:
            self.tree.delete(selected_item)
            print("Data terhapus")
        else:
            print("Pilih data yang ingin dihapus.")

    def kembali(self):
        print("Kembali ke halaman sebelumnya")

if __name__ == "__main__":
    window = Tk()
    app = AplikasiPenjual(window)
    window.mainloop()
