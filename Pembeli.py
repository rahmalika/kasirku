import tkinter as tk
from tkinter import CENTER, StringVar #membuat teks atau widget lain (seperti Label atau Entry)
from tkinter import ttk, messagebox
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from tkinter import messagebox


# Membaca data barang dari file CSV
data_barang = pd.read_csv("data_barang.csv")

# Fungsi untuk mencari barang berdasarkan kode
def cari_barang(kode):
    barang = data_barang[data_barang['kode_barang'] == kode]
    if not barang.empty:
        return barang.iloc[0].to_dict()
    else:
        return None

# Fungsi untuk menambah barang ke dalam daftar transaksi
def tambah_barang():
    kode = kode_entry.get()
    jumlah = jumlah_entry.get()

    if not jumlah.isdigit():
        messagebox.showerror("Input Tidak Valid", "Jumlah harus berupa angka.")
        return
    
    if not kode:
        messagebox.showerror("Input Tidak Valid", "Kode harus diisi.")
        return

    if not cari_barang(kode):
        messagebox.showerror("Kode Tidak Ditemukan", f"Barang dengan kode {kode} tidak ditemukan.")
        return
    

    jumlah = int(jumlah)

    barang = cari_barang(kode)
    if barang:
        nama = barang['nama_barang']
        harga = barang['harga']
        stock = barang['stock']

        if jumlah > stock:
            messagebox.showwarning("Stok Tidak Cukup", f"Stok untuk {nama} tidak mencukupi. Stok tersedia: {stock}")
        else:
            subtotal = harga * jumlah
            daftar_transaksi.insert("", "end", values=(kode, nama, harga, jumlah, subtotal))
            messagebox.showinfo("Barang Ditambahkan", f"{nama} sebanyak {jumlah} berhasil ditambahkan ke transaksi.")
            update_total()
    else:
        messagebox.showerror("Kode Tidak Ditemukan", f"Barang dengan kode {kode} tidak ditemukan.")
    

    kode_entry.delete(0, tk.END)
    jumlah_entry.delete(0, tk.END)


# Fungsi untuk memperbarui total harga
def update_total():
    total = 0
    for item in daftar_transaksi.get_children():
        total += daftar_transaksi.item(item)['values'][4]  # Ambil subtotal
    total_label.config(text=f"Total Harga (Rp): {total}")

# Fungsi untuk mencetak invoice
def print_invoice():
    # Menghitung total
    total = sum(daftar_transaksi.item(item)['values'][4] for item in daftar_transaksi.get_children())
    
    if total == 0:
        messagebox.showwarning("Tidak Ada Data", "Tidak ada data untuk dicetak.")
        return

    # Nama file PDF
    filename = "invoice.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Pengaturan layout
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "INVOICE")
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Total Harga: Rp {total}")

    # Detail informasi
    y = 700
    c.setFont("Helvetica", 10)
    c.drawString(100, y, "Kode         Nama                     Harga       Jumlah   Subtotal")
    y -= 20

    # Loop untuk menampilkan daftar transaksi
    for item in daftar_transaksi.get_children():
        if y < 50:  # Cek apakah cukup di halaman ini, jika tidak, buat halaman baru
            c.showPage()
            c.setFont("Helvetica", 10)
            y = 750
            c.drawString(100, y, "Kode         Nama                     Harga       Jumlah   Subtotal")
            y -= 20
        
        values = daftar_transaksi.item(item)['values']
        c.drawString(100, y, f"{values[0]:<10} {values[1]:<25} Rp {values[2]:<8} {values[3]:<7} Rp {values[4]}")
        y -= 20

    # Subtotal, Diskon, Pajak, dan Total
    subtotal = total
    discount = 0  # Set diskon sesuai kebutuhan
    tax = subtotal * 0.1  # Misalnya, pajak 10%
    grand_total = subtotal - discount + tax

    y -= 40
    c.setFont("Helvetica-Bold", 10)
    c.drawString(100, y, f"Subtotal: Rp {subtotal}")
    y -= 20
    c.drawString(100, y, f"Diskon: Rp {discount}")
    y -= 20
    c.drawString(100, y, f"Pajak (10%): Rp {tax}")
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y, f"Total Akhir: Rp {grand_total}")

    # Simpan file PDF
    c.save()
    messagebox.showinfo("Invoice Disimpan", f"Invoice disimpan sebagai {filename}")

#halaman pembayaran
def halaman_pembayaran(window_landing_page, landing_page):
   # Menghapus konten lama
    for widget in window_landing_page.winfo_children():
        widget.destroy()

    # Judul
    title = tk.Label(window_landing_page, text="Halaman Pembayaran", font=("Times New Roman", 24), bg="#f7f3e8")
    title.pack(pady=10)

    # Pilih metode pembayaran
    payment_method = StringVar(value="Tunai")
    tk.Label(window_landing_page, text="Pilih Metode Pembayaran:").pack()

    # Radio button untuk memilih metode pembayaran
    tk.Radiobutton(window_landing_page, text="Tunai", variable=payment_method, value="Tunai").pack()
    tk.Radiobutton(window_landing_page, text="Transfer", variable=payment_method, value="Transfer").pack()

    # Frame untuk opsi pembayaran
    payment_frame = tk.Frame(window_landing_page)
    payment_frame.pack(pady=10)

    # Fungsi untuk menampilkan opsi pembayaran berdasarkan metode
    def update_payment_options():
        for widget in payment_frame.winfo_children():
            widget.destroy()
        
        if payment_method.get() == "Tunai":
            tk.Label(payment_frame, text="Masukkan Nominal Uang Tunai:").pack()
            nominal_entry = tk.Entry(payment_frame)
            nominal_entry.pack()

            def confirm_cash_payment():
                nominal = nominal_entry.get()
                if nominal.isdigit():
                    nominal = int(nominal)
                    total = sum(daftar_transaksi.item(item)['values'][4] for item in daftar_transaksi.get_children())
                    if nominal >= total:
                        change = nominal - total
                        messagebox.showinfo("Kembalian", f"Pembayaran berhasil. Kembalian: Rp {change}")
                        print_invoice()
                    else:
                        messagebox.showerror("Error", "Nominal uang kurang dari total harga.")
                else:
                    messagebox.showerror("Input Tidak Valid", "Masukkan nominal berupa angka.")
            
            confirm_button = tk.Button(payment_frame, text="Konfirmasi Pembayaran", command=confirm_cash_payment)
            confirm_button.pack(pady=10)

        elif payment_method.get() == "Transfer":
            tk.Label(payment_frame, text="Silakan Transfer ke Nomor Rekening: 1234567890").pack()
            tk.Label(payment_frame, text="atau Scan Kode QR berikut:").pack()
            # (Tambahkan gambar QR code jika tersedia)
            qr_placeholder = tk.Label(payment_frame, text="[QR CODE]", bg="gray", width=20, height=10)
            qr_placeholder.pack(pady=10)

            def confirm_transfer_payment():
                messagebox.showinfo("Pembayaran Transfer", "Transfer berhasil dikonfirmasi.")
                print_invoice()

            confirm_button = tk.Button(payment_frame, text="Konfirmasi Pembayaran Transfer", command=confirm_transfer_payment)
            confirm_button.pack(pady=10)
            payment_method.trace("w", lambda *args: update_payment_options())
            update_payment_options()
        
        

# Fungsi untuk menampilkan halaman pembeli
def halaman_pembeli(window_landing_page, landing_page):
    # Menghapus konten lama
    for widget in window_landing_page.winfo_children():
        widget.destroy()
    
    # Judul
    title = tk.Label(window_landing_page, text="Halaman Transaksi", font=("Times New Roman", 24), bg="#f7f3e8")
    title.pack(pady=10)

    # Input Kode Barang
    tk.Label(window_landing_page, text="Kode Barang:").pack()
    global kode_entry
    kode_entry = tk.Entry(window_landing_page)
    kode_entry.pack()

    # Input Jumlah Barang
    tk.Label(window_landing_page, text="Jumlah:").pack()
    global jumlah_entry
    jumlah_entry = tk.Entry(window_landing_page)
    jumlah_entry.pack()

    # Tombol Tambah Barang
    tambah_button = tk.Button(window_landing_page, text="Tambah", command=tambah_barang)
    tambah_button.pack(pady=10)

    # Tabel untuk daftar transaksi
    global daftar_transaksi
    columns = ("Kode", "Nama Barang", "Harga", "Jumlah", "Sub Total")
    daftar_transaksi = ttk.Treeview(window_landing_page, columns=columns, show="headings")
    for col in columns:
        daftar_transaksi.heading(col, text=col)
    daftar_transaksi.pack(fill="both", expand=True)

    # Label untuk total harga
    global total_label
    total_label = tk.Label(window_landing_page, text="Total Harga (Rp): 0", bg="#f7f3e8", font=("Times New Roman", 12))
    total_label.pack(pady=10)

    # Tombol Cetak Invoice
    print_button = tk.Button(window_landing_page, text="Cetak Invoice", command=halaman_pembayaran, width=15)
    print_button.pack(pady=10)

    # Tombol Kembali
    tombol_kembali = tk.Button(window_landing_page, text="Kembali", command=landing_page, font=("Arial", 14), bg="#3bdfff", fg="black", width=10, height=2)
    tombol_kembali.pack(pady=20)

    # Footer informasi
    footer = tk.Label(window_landing_page, text="©2024 | Rahmatika Aumara Zilka 165231005", font=("Times New Roman", 10), bg="#0CC9CC", fg="white")
    footer.pack(side="bottom", fill="x")

# Fungsi untuk menampilkan halaman transaksi
def halaman_transaksi(window_landing_page, landing_page):
    # Menghapus konten lama
    for widget in window_landing_page.winfo_children():
        widget.destroy()

    # Menampilkan teks judul
    text = tk.Label(window_landing_page, text="Halaman Pembeli", bg="#23C9FF", fg="white", font=("Poppins", 30))
    text.pack(pady=20)

    # Memanggil fungsi halaman pembeli
    halaman_pembeli(window_landing_page, landing_page)

# Inisialisasi GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplikasi Kasir")
    root.geometry("800x600")
    landing_page = lambda: None  # Placeholder for the landing page function
    halaman_transaksi(root, landing_page)
    root.mainloop()
