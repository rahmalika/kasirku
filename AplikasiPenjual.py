from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
import os
import uuid
class AplikasiPenjual:
    def __init__(self, window):
        self.window = window
        self.window.title("KasirKu - Data Barang")
        self.window.geometry("800x600")
        self.window.configure(bg="#FFF2DB")

        # Nama file CSV
        self.csv_file = "data_barang.csv"

        # Membaca data dari CSV ke dalam DataFrame
        self.load_data_csv()

        # Halaman utama
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
        columns = ("kode_barang", "nama_barang", "stock", "harga")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=10)
        self.tree.heading("kode_barang", text="Kode Barang")
        self.tree.heading("nama_barang", text="Nama Barang")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("harga", text="Harga")
        self.tree.column("kode_barang", width=100, anchor=CENTER)
        self.tree.column("nama_barang", width=200, anchor=CENTER)
        self.tree.column("stock", width=100, anchor=CENTER)
        self.tree.column("harga", width=150, anchor=CENTER)
        self.tree.place(relx=0.5, rely=0.4, anchor=CENTER)

        # Menampilkan data ke dalam Treeview
        self.display_data()

        # Tombol Edit
        self.tombol_edit = Button(
            self.window, text="Edit", font=("Arial", 12), bg="#3bdfff", fg="black",
            width=10, height=2, relief="flat", command=self.open_edit_data
        )
        self.tombol_edit.place(relx=0.2, rely=0.8, anchor=CENTER)

        # Tombol Tambah
        self.tombol_tambah = Button(
            self.window, text="Tambah", font=("Arial", 12), bg="#3bdfff", fg="black",
            width=10, height=2, relief="flat", command=self.open_tambah_data
        )
        self.tombol_tambah.place(relx=0.5, rely=0.8, anchor=CENTER)

        # Tombol Hapus
        self.tombol_hapus = Button(
            self.window, text="Hapus", font=("Arial", 12), bg="red", fg="white",
            width=10, height=2, relief="flat", command=self.hapus_data
        )
        self.tombol_hapus.place(relx=0.8, rely=0.8, anchor=CENTER)

    def load_data_csv(self):
        # Memuat data dari CSV ke dalam DataFrame
        try:
            if os.path.exists(self.csv_file):
                self.df = pd.read_csv(self.csv_file)
            else:
                # Jika file tidak ada, buat DataFrame kosong
                self.df = pd.DataFrame(columns=["kode_barang", "nama_barang", "stock", "harga"])
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {e}")

    def display_data(self):
        # Menampilkan data dari DataFrame ke dalam Treeview
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)
            for _, row in self.df.iterrows():
                harga = f"Rp {row['harga']:.0f}"
                stok = int(row['stock'])
                self.tree.insert("", "end", values=(row["kode_barang"], row["nama_barang"], stok, harga))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menampilkan data: {e}")

    def simpan_data_csv(self):
        # Simpan DataFrame ke file CSV
        try:
            self.df.to_csv(self.csv_file, index=False)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {e}")

    def open_tambah_data(self):
        # Membuka halaman untuk menambahkan data
        try:
            self.halaman_tambah_data("Tambah Data")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka halaman tambah data: {e}")

    def halaman_tambah_data(self, title, data=None):
        # Membuat halaman tambah data dengan form input
        try:
            self.new_window = Toplevel(self.window)
            self.new_window.title(title)
            self.new_window.geometry("400x400")
            self.new_window.configure(bg="#FFF2DB")

            Label(self.new_window, text="Nama Barang:", bg="#FFF2DB").pack(pady=5)
            self.nama_barang_entry = Entry(self.new_window, width=30)
            self.nama_barang_entry.pack(pady=5)

            Label(self.new_window, text="Quantity:", bg="#FFF2DB").pack(pady=5)
            self.stok_entry = Entry(self.new_window, width=30)
            self.stok_entry.pack(pady=5)

            Label(self.new_window, text="Harga:", bg="#FFF2DB").pack(pady=5)
            self.harga_entry = Entry(self.new_window, width=30)
            self.harga_entry.pack(pady=5)

            # Jika data untuk edit ada, isi form dengan data lama
            if data:
                self.nama_barang_entry.insert(0, data[1])
                self.stok_entry.insert(0, data[2])
                self.harga_entry.insert(0, data[3])

            Button(self.new_window, text="Simpan", bg="#3bdfff", command=lambda: self.tambah_data(data)).pack(pady=20)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat halaman tambah data: {e}")

    def tambah_data(self, data=None):
        # Mendapatkan data dari form
        try:
            nama = self.nama_barang_entry.get()
            stok = self.stok_entry.get()
            harga = self.harga_entry.get()

            if not (nama and stok.isdigit() and harga.isdigit()):
                messagebox.showwarning("Input Error", "Pastikan semua data valid.")
                return

            if data:
                # Edit data di DataFrame
                self.df.loc[self.df["kode_barang"] == data[0], ["nama_barang", "stock", "harga"]] = [nama, int(stok), int(harga)]
            else:
                # Tambah data baru
                kode_barang = str(uuid.uuid5(uuid.NAMESPACE_DNS, nama)).replace('-', '')[:5].upper(
                    
                )
                new_row = {"kode_barang": kode_barang, "nama_barang": nama, "stock": int(stok), "harga": int(harga)}
                self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

            self.simpan_data_csv()  # Simpan perubahan ke CSV
            self.display_data()     # Update Treeview
            self.new_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah atau mengedit data: {e}")

    def open_edit_data(self):
        # Membuka halaman edit data
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Edit Error", "Pilih data yang ingin diedit.")
                return
            data = self.tree.item(selected_item[0], 'values')
            self.halaman_tambah_data("Edit Data", data)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka halaman edit data: {e}")

    def open_hapus_data(self):
        # Membuka halaman hapus data
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Hapus Error", "Pilih data yang ingin dihapus.")
                return
            data = self.tree.item(selected_item[0], 'values')
            self.halaman_tambah_data("Hapus Data", data)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka halaman hapus data: {e}")


    def hapus_data(self):
        # Menghapus data dari DataFrame
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Hapus Error", "Pilih data yang ingin dihapus.")
                return
            confirm = messagebox.askyesno("Hapus Data", "Apakah Anda yakin ingin menghapus data ini?")
            if not confirm: 
                return
            
            data = self.tree.item(selected_item[0], 'values')
            self.df = self.df[self.df["kode_barang"] != data[0]]
            self.simpan_data_csv()
            self.display_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def format_rupiah(angka):
    # Fungsi untuk memformat angka menjadi Rupiah
        return f"Rp {angka:,.0f}".replace(",", ".")



if __name__ == "__main__":
    window = Tk()
    app = AplikasiPenjual(window)
    window.mainloop()
