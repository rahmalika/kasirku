import tkinter as tk
from tkinter import CENTER

def halaman_penjual(window_landing_page, landing_page):
    # Menghapus konten lama
    for widget in window_landing_page.winfo_children():
        widget.destroy()
    
    # Menampilkan teks dan tombol kembali
    text = tk.Label(window_landing_page, text="Halaman Penjual", bg="#23C9FF", fg="white", font=("Poppins", 30))
    text.pack(pady=50)

    tombol_kembali = tk.Button(window_landing_page, text="Kembali", command=landing_page, font=("Arial", 14), bg="#3bdfff", fg="black", width=10, height=2)
    tombol_kembali.place(relx=0.5, rely=0.6, anchor=CENTER)

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


    # fungsi simpan data
    def simpan_data_barang():
        
        nama_barang = entry_nama_barang.get()
        quantity = entry_quantity.get()

          # Validasi input
        if not nama_barang or not quantity:
            text.showwarning("Peringatan", "Nama barang dan quantity harus diisi!")
            return

        # Tampilkan data barang yang diinput (atau bisa simpan ke database)
        text.showinfo("Data Barang", f"Nama Barang: {nama_barang}\nQuantity: {quantity}")

    # Tombol Simpan
    tombol_simpan = tk.Button(window_landing_page, text="Simpan", command=simpan_data_barang, font=("Arial", 12), bg="#3bdfff", fg="black", width=10)
    tombol_simpan.pack(pady=20)

 # Tombol Kembali
    tombol_kembali = tk.Button(window_landing_page, text="Kembali", command=lambda: kembali_ke_landing_page(window_landing_page, window_landing_page), font=("Arial", 12), bg="#3bdfff", fg="black", width=10)
    tombol_kembali.pack(pady=10)

def kembali_ke_landing_page(window_penjual, window_landing_page):
    # Tutup halaman penjual dan kembali ke halaman utama
    window_penjual.destroy()
    window_landing_page.deiconify()