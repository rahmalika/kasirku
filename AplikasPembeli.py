import tkinter as tk
from tkinter import messagebox, ttk, StringVar, IntVar
import pandas as pd
from datetime import datetime

class AplikasiPembeli:
    def __init__(self, root, csv_file="data_barang.csv"):
        self.root = root
        self.root.title("Halaman Transaksi")
        self.root.geometry("800x600")
        self.csv_file = csv_file
        self.df = pd.read_csv(self.csv_file) if pd.io.common.file_exists(csv_file) else pd.DataFrame(columns=["kode_barang", "nama_barang", "stock", "harga"])

        # Variabel transaksi
        self.nomor_penjualan = StringVar(value=str(datetime.now().strftime("%Y%m%d%H%M%S")))
        self.tanggal_transaksi = StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.kode_barang = StringVar()
        self.quantity = IntVar()
        self.total_belanja = 0
        self.daftar_barang = []
        
        # Frame Transaksi
        self.create_transaction_frame()
        
        # Frame Daftar Barang
        self.create_daftar_barang_frame()
        
        # Frame Pembayaran
        self.create_payment_frame()
        
        # Frame Total dan Button Invoice
        self.create_total_frame()
        
    def create_transaction_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        tk.Label(frame, text="DATA TRANSAKSI").grid(row=0, column=0, columnspan=2)
        tk.Label(frame, text="Nomor Penjualan").grid(row=1, column=0, sticky="w")
        tk.Label(frame, textvariable=self.nomor_penjualan).grid(row=1, column=1, sticky="w")
        tk.Label(frame, text="Tanggal Transaksi").grid(row=2, column=0, sticky="w")
        tk.Label(frame, textvariable=self.tanggal_transaksi).grid(row=2, column=1, sticky="w")
        
        # Input Kode Barang
        tk.Label(frame, text="INPUT BARANG").grid(row=3, column=0, columnspan=2)
        tk.Label(frame, text="Kode Barang").grid(row=4, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.kode_barang).grid(row=4, column=1, sticky="w")
        
        tk.Label(frame, text="Quantity").grid(row=5, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.quantity).grid(row=5, column=1, sticky="w")
        
        tk.Button(frame, text="Tambah Barang", command=self.tambah_barang).grid(row=6, column=0, columnspan=2)
        
    def create_daftar_barang_frame(self):
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(pady=10)
        
        tk.Label(self.tree_frame, text="DAFTAR BARANG").pack()
        columns = ["No", "Kode", "Nama Barang", "Harga (Rp)", "Quantity", "Sub Total (Rp)"]
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack()
    
    def create_payment_frame(self):
        self.payment_frame = tk.Frame(self.root)
        self.payment_frame.pack(pady=10)
        
        tk.Label(self.payment_frame, text="Metode Pembayaran").pack()
        
        self.payment_method = StringVar(value="tunai")
        tk.Radiobutton(self.payment_frame, text="Tunai", variable=self.payment_method, value="tunai", command=self.update_payment_option).pack(anchor="w")
        tk.Radiobutton(self.payment_frame, text="Transfer", variable=self.payment_method, value="transfer", command=self.update_payment_option).pack(anchor="w")
        
        # Input Nominal untuk Tunai dan No Rekening untuk Transfer
        self.nominal_entry = tk.Entry(self.payment_frame)
        self.nominal_label = tk.Label(self.payment_frame, text="Nominal Uang (Rp)")
        
        self.rekening_options = ["Bank A - 1234567890", "Bank B - 0987654321", "Bank C - 1122334455"]
        self.rekening_var = StringVar(value=self.rekening_options[0])
        self.rekening_dropdown = ttk.Combobox(self.payment_frame, textvariable=self.rekening_var, values=self.rekening_options, state="readonly")
        
        # Tampilkan opsi pembayaran pertama kali (default: tunai)
        self.update_payment_option()

    def create_total_frame(self):
        total_frame = tk.Frame(self.root)
        total_frame.pack(pady=10)
        
        self.total_label = tk.Label(total_frame, text="Grand Total Belanja: Rp 0")
        self.total_label.pack()
        
        tk.Button(total_frame, text="Lakukan Pembayaran", command=self.proses_pembayaran).pack()
        
    def tambah_barang(self):
        kode = self.kode_barang.get()
        qty = self.quantity.get()
        
        if kode and qty > 0:
            # Cari barang berdasarkan kode
            barang = self.df[self.df["kode_barang"] == kode]
            
            if not barang.empty:
                nama_barang = barang.iloc[0]["nama_barang"]
                harga = barang.iloc[0]["harga"]
                subtotal = harga * qty
                self.total_belanja += subtotal
                
                # Tambah barang ke daftar
                self.daftar_barang.append({
                    "kode_barang": kode,
                    "nama_barang": nama_barang,
                    "harga": harga,
                    "quantity": qty,
                    "subtotal": subtotal
                })
                
                # Tampilkan di Treeview
                self.tree.insert("", "end", values=(len(self.daftar_barang), kode, nama_barang, f"{harga:,.0f}", qty, f"{subtotal:,.0f}"))
                self.total_label.config(text=f"Grand Total Belanja: Rp {self.total_belanja:,.0f}")
                
                # Reset input
                self.kode_barang.set("")
                self.quantity.set(0)
            else:
                messagebox.showwarning("Barang Tidak Ditemukan", "Kode barang tidak ditemukan di data.")
        else:
            messagebox.showwarning("Input Error", "Kode Barang dan Quantity harus diisi.")

    def update_payment_option(self):
        if self.payment_method.get() == "tunai":
            # Tampilkan input nominal untuk tunai, sembunyikan rekening
            self.rekening_dropdown.pack_forget()
            self.nominal_label.pack()
            self.nominal_entry.pack()
        elif self.payment_method.get() == "transfer":
            # Tampilkan dropdown rekening bank, sembunyikan input nominal
            self.nominal_label.pack_forget()
            self.nominal_entry.pack_forget()
            self.rekening_dropdown.pack()

    def proses_pembayaran(self):
        if not self.daftar_barang:
            messagebox.showwarning("Daftar Kosong", "Tidak ada barang untuk diproses.")
            return

        if self.payment_method.get() == "tunai":
            try:
                nominal_uang = int(self.nominal_entry.get().replace(".", ""))
                if nominal_uang < self.total_belanja:
                    messagebox.showwarning("Pembayaran Tidak Cukup", "Uang yang diberikan tidak mencukupi total belanja.")
                    #return
                kembalian = nominal_uang - self.total_belanja
                messagebox.showinfo("Pembayaran Tunai", f"Pembayaran berhasil! Kembalian: Rp {kembalian:,.0f}")
            except ValueError:
                messagebox.showwarning("Input Error", "Masukkan nominal uang yang valid.")
                return
        else:
            # Untuk transfer, tampilkan konfirmasi rekening bank
            selected_bank = self.rekening_var.get()
            confirmation = messagebox.askyesno("Konfirmasi Pembayaran", f"Anda memilih transfer ke {selected_bank}. Lanjutkan?")
            if confirmation:
                messagebox.showinfo("Pembayaran Transfer", "Pembayaran melalui transfer berhasil. Silakan cek rekening Anda.")
        
        # Setelah pembayaran selesai, cetak invoice
        self.print_invoice()

    def print_invoice(self):
        # Simulasi proses mencetak invoice
        invoice = f"Nomor Penjualan: {self.nomor_penjualan.get()}\nTanggal: {self.tanggal_transaksi.get()}\n"
        invoice += "------------------------------------\n"
        for i, barang in enumerate(self.daftar_barang, start=1):
            invoice += f"{i}. {barang['nama_barang']} - Rp {barang['harga']:,} x {barang['quantity']} = Rp {barang['subtotal']:,}\n"
        invoice += "------------------------------------\n"
        invoice += f"GRAND TOTAL: Rp {self.total_belanja:,.0f}\n"
        invoice += f"Metode Pembayaran: {self.payment_method.get()}\n"
        
        if self.payment_method.get() == "tunai":
            nominal_uang = int(self.nominal_entry.get().replace(".", ""))
            kembalian = nominal_uang - self.total_belanja
            invoice += f"Uang Diberikan: Rp {nominal_uang:,.0f}\nKembalian: Rp {kembalian:,.0f}"
        else:
            invoice += f"Rekening Tujuan: {self.rekening_var.get()}"
        
        # Tampilkan invoice di messagebox (untuk simulasi)
        messagebox.showinfo("Invoice", invoice)

        # Reset total dan daftar barang setelah pembayaran
        self.total_belanja = 0
        self.daftar_barang.clear()
        self.tree.delete(*self.tree.get_children())
        self.total_label.config(text="Grand Total Belanja: Rp 0")

# Inisialisasi aplikasi
root = tk.Tk()
app = AplikasiPembeli(root)
root.mainloop()
