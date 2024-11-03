import uuid
import tkinter as tk
from tkinter import ttk, CENTER
import tkinter.messagebox as msg
import pandas as pd
import csv

def halaman_penjual(window_landing_page, landing_page):
    for widget in window_landing_page.winfo_children():
        widget.destroy()

    # Judul halaman
    text = tk.Label(window_landing_page, text="Data Barang", bg="#23C9FF", fg="white", font=("Poppins", 30))
    text.pack(pady=20)

    # Membuat Treeview untuk tabel
    tree = ttk.Treeview(window_landing_page, columns=("kode_barang", "nama_barang", "stock", "harga"), show="headings")
    tree.heading("kode_barang", text="Kode Barang")
    tree.heading("nama_barang", text="Nama Barang")
    tree.heading("stock", text="Stock")
    tree.heading("harga", text="Harga")
    tree.pack(pady=10)

    # Fungsi untuk menampilkan data di Treeview
    def tampilkan_data():
        tree.delete(*tree.get_children())
        try:
            df = pd.read_csv('data_barang.csv')
            for index, row in df.iterrows():
                tree.insert("", "end", values=(row["kode_barang"], row["nama_barang"], row["stock"], row["harga"]))
        except FileNotFoundError:
            msg.showerror("Error", "File data_barang.csv tidak ditemukan.")

    # Fungsi untuk mengedit data
    def edit_data():
        selected_item = tree.selection()
        if not selected_item:
            msg.showwarning("Peringatan", "Pilih data yang ingin diedit.")
            return

        item_data = tree.item(selected_item, "values")
        kode_barang, nama_barang, stock, harga = item_data[:4]

        # Membuat jendela edit
        edit_window = tk.Toplevel(window_landing_page)
        edit_window.title("Edit Data")
        edit_window.geometry("700x400")

        tk.Label(edit_window, text="Nama Barang:").pack()
        entry_nama = tk.Entry(edit_window)
        entry_nama.insert(0, nama_barang)
        entry_nama.pack()

        tk.Label(edit_window, text="Stock:").pack()
        entry_stock = tk.Entry(edit_window)
        entry_stock.insert(0, stock)
        entry_stock.pack()

        tk.Label(edit_window, text="Harga:").pack()
        entry_harga = tk.Entry(edit_window)
        entry_harga.insert(0, harga)
        entry_harga.pack()

        def simpan_perubahan():
            new_nama_barang = entry_nama.get()
            new_stock = entry_stock.get()
            new_harga = entry_harga.get()

            # Memperbarui data CSV
            df = pd.read_csv('data_barang.csv')
            df.loc[df['kode_barang'] == kode_barang, ['nama_barang', 'stock', 'harga']] = [new_nama_barang, new_stock, new_harga]
            df.to_csv('data_barang.csv', index=False)
            edit_window.destroy()
            tampilkan_data()

        tk.Button(edit_window, text="Simpan", command=simpan_perubahan).pack(pady=10)

    # Fungsi untuk menghapus data
    def hapus_data():
        selected_item = tree.selection()
        if not selected_item:
            msg.showwarning("Peringatan", "Pilih data yang ingin dihapus.")
            return

        item_data = tree.item(selected_item, "values")
        kode_barang = item_data[0]

        # Konfirmasi penghapusan
        if msg.askyesno("Hapus Data", "Apakah Anda yakin ingin menghapus data ini?"):
            df = pd.read_csv('data_barang.csv')
            df = df[df['kode_barang'] != kode_barang]
            df.to_csv('data_barang.csv', index=False)
            tampilkan_data()

    # Tombol Edit dan Hapus
    tombol_edit = tk.Button(window_landing_page, text="Edit", command=edit_data, font=("Arial", 12), bg="#3bdfff", fg="black", width=10)
    tombol_edit.pack(side="left", padx=20, pady=10)
    
    tombol_hapus = tk.Button(window_landing_page, text="Hapus", command=hapus_data, font=("Arial", 12), bg="#ff3b3b", fg="black", width=10)
    tombol_hapus.pack(side="right", padx=20, pady=10)

    # Tampilkan data awal
    tampilkan_data()

    # Tombol kembali ke halaman utama
    tombol_kembali = tk.Button(window_landing_page, text="Kembali", command=landing_page, font=("Arial", 14), bg="#3bdfff", fg="black", width=10, height=2)
    tombol_kembali.place(relx=0.5, rely=0.9, anchor=CENTER)


    

def halaman_input_barang(window_landing_page, landing_page):
# Menghapus konten lama
    for widget in window_landing_page.winfo_children():
        widget.destroy()
    
    # Menampilkan teks dan tombol kembali
    text = tk.Label(window_landing_page, text="Halaman Penjual", bg="#23C9FF", fg="white", font=("Poppins", 30))
    text.pack(pady=50)

    tombol_kembali = tk.Button(window_landing_page, text="Kembali", command=landing_page, font=("Arial", 14), bg="#3bdfff", fg="black", width=10, height=2)
    tombol_kembali.place(relx=0.5, rely=0.8, anchor=CENTER)

    # Input nama barang
    label_nama_barang = tk.Label(window_landing_page, text="Nama Barang:", font=("Arial", 12))
    label_nama_barang.pack()
    entry_nama_barang = tk.Entry(window_landing_page, font=("Arial", 12), width=30)
    entry_nama_barang.pack(pady=5)
    
    # Input qty barang
    label_quantity = tk.Label(window_landing_page, text="Quantity:", font=("Arial", 12))
    label_quantity.pack()
    entry_quantity = tk.Entry(window_landing_page, font=("Arial", 12), width=30)
    entry_quantity.pack(pady=5)


    #input harga
    label_harga = tk.Label(window_landing_page, text="Harga:", font=("Arial", 12))
    label_harga.pack()
    entry_harga = tk.Entry(window_landing_page, font=("Arial", 12), width=30)
    entry_harga.pack(pady=5)

    def membuatKodeAcak(input_string):
        unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, input_string)
        unique_code = str(unique_id).replace('-', '')[:5].upper()
        return unique_code

    # fungsi simpan data
    def simpan_data_barang():
        nama_barang = entry_nama_barang.get()
        kode_barang = membuatKodeAcak(nama_barang)
        quantity = entry_quantity.get()
        harga = entry_harga.get()

          # Validasi input
        if not nama_barang or not quantity:
            msg.showerror("Error", "Nama barang dan quantity harus diisi.")
            return

    #tambahkan ke csv
        with open("data_barang.csv", "a", newline="") as file:
            writer = csv.writer(file)

            # Menulis data ke CSV
            writer.writerow([kode_barang, nama_barang, quantity, harga])

        # Tampilkan data barang yang diinput (atau bisa simpan ke database)
        msg.showinfo("Sukses", "Data barang berhasil disimpan.")
        #setelah barang disumpan input kembali kosong
        entry_nama_barang.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_harga.delete(0, tk.END)



    # Tombol Simpan
    tombol_simpan = tk.Button(window_landing_page, text="Simpan", command=simpan_data_barang, font=("Arial", 12), bg="#3bdfff", fg="black", width=10)
    tombol_simpan.pack(pady=20)
def kembali_ke_landing_page(window_penjual, window_landing_page):
    # Tutup halaman penjual dan kembali ke halaman utama
    window_penjual.destroy()
    window_landing_page.deiconify()

