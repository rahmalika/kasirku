import csv
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Label, Scrollbar, VERTICAL, Toplevel, Radiobutton, StringVar, messagebox
from tkinter.ttk import Treeview, Style
from PIL import Image, ImageTk
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime


class PelangganApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x720")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.ASSETS_PATH = Path(r"E:\UTS_PEMKOM\build\assets\frame4")
        self.image_refs = []  # Menyimpan referensi gambar untuk mencegah penghapusan oleh garbage collector

        # Load data barang dari CSV
        self.data_barang = self.load_data_barang()
        # Daftar barang yang ditambahkan
        self.cart = []

        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        """Mendapatkan path relatif untuk file aset."""
        return self.ASSETS_PATH / Path(path)

    def load_data_barang(self):
        """Membaca data barang dari file CSV."""
        data = {}
        with open("data_barang.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data[row["kode_barang"]] = row
        return data

    def setup_ui(self):
        """Menyusun elemen-elemen UI dengan placeholder di input dan penataan rapi."""
        # Canvas
        self.canvas = Canvas(
            self.root,
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

        # Tambahkan teks judul
        self.canvas.create_text(
            140.0, 50.0, anchor="nw",
            text="Hallo, Pelanggan yang baik!",
            fill="#FFFFF2",  # Tetap menggunakan warna putih sesuai desain Anda
            font=("Poppins ExtraBold", 36 * -1)
        )
        self.canvas.create_text(
            140.0, 120.0, anchor="nw",
            text="Silakan masukkan kode barang dan jumlah yang kamu beli",
            fill="#FFFFF2",
            font=("Poppins SemiBold", 18 * -1)
        )

        # Entry untuk kode barang (dengan placeholder)
        self.entry_kode = self.create_centered_entry(140, 200, "Kode Barang")
        self.entry_jumlah = self.create_centered_entry(360, 200, "Jumlah")

        # Tombol aksi
        self.create_button(140.0, 270.0, "button_1.png", 120, 40, self.on_tambah_click)  # Tambah
        self.create_button(280.0, 270.0, "button_4.png", 120, 40, self.on_edit_click)    # Edit
        self.create_button(420.0, 270.0, "button_2.png", 120, 40, self.on_batal_click)   # Batal
        self.create_button(560.0, 270.0, "button_3.png", 120, 40, self.on_selesai_click) # Selesai

        # Tabel dengan scrollbar untuk daftar barang
        self.setup_treeview()

        # Label total di bawah tabel
        self.total_label = Label(self.root, text="Total: Rp 0", font=("Poppins", 14, "bold"), bg="#FFFFFF", fg="#000716")
        self.total_label.place(x=800, y=550)

    def create_centered_entry(self, x, y, placeholder_text):
        """Membuat entry dengan placeholder yang terpusat."""
        entry = Entry(self.root, bd=2, font=("Poppins", 12), justify="center", fg="#A0A0A0")  # Placeholder dengan warna abu-abu
        entry.insert(0, placeholder_text)
        entry.bind("<FocusIn>", lambda event, e=entry, t=placeholder_text: self.clear_placeholder(e, t))
        entry.bind("<FocusOut>", lambda event, e=entry, t=placeholder_text: self.add_placeholder(e, t))
        entry.place(x=x, y=y, width=200, height=30)
        return entry

    def setup_treeview(self):
        """Membuat Treeview sebagai tabel dengan scrollbar untuk menampilkan daftar barang."""
        style = Style()
        style.configure("Treeview.Heading", font=("Poppins", 10, "bold"))
        style.configure("Treeview", font=("Poppins", 10), rowheight=25)

        # Membuat scrollbar vertikal
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL)

        self.tree = Treeview(
            self.root,
            columns=("Kode", "Nama", "Jumlah", "Harga Satuan", "Total"),
            show='headings',
            height=8,
            yscrollcommand=self.scrollbar.set
        )
        self.scrollbar.config(command=self.tree.yview)
        self.scrollbar.place(x=980, y=340, height=200)

        # Menambahkan kolom dengan pengaturan posisi
        self.tree.heading("Kode", text="Kode")
        self.tree.heading("Nama", text="Nama")
        self.tree.heading("Jumlah", text="Jumlah")
        self.tree.heading("Harga Satuan", text="Harga Satuan")
        self.tree.heading("Total", text="Total")

        self.tree.column("Kode", anchor="center", width=100)
        self.tree.column("Nama", anchor="w", width=300)
        self.tree.column("Jumlah", anchor="center", width=80)
        self.tree.column("Harga Satuan", anchor="e", width=100)
        self.tree.column("Total", anchor="e", width=100)

        self.tree.place(x=110, y=340)

    def add_image(self, file_name, x, y):
        image = PhotoImage(file=self.relative_to_assets(file_name))
        self.image_refs.append(image)
        self.canvas.create_image(x, y, image=image)

    def create_button(self, x, y, image_file, width, height, command):
        button_image = PhotoImage(file=self.relative_to_assets(image_file))
        self.image_refs.append(button_image)
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        button.place(x=x, y=y, width=width, height=height)

    def on_tambah_click(self):
        """Menambahkan barang berdasarkan kode dan jumlah yang diinput."""
        kode_barang = self.entry_kode.get()
        jumlah = self.entry_jumlah.get()

        if not jumlah.isdigit():
            messagebox.showerror("Error", "Jumlah harus berupa angka!")
            return

        jumlah = int(jumlah)

        for item in self.cart:
            if item["kode"] == kode_barang:
                messagebox.showerror("Error", "Barang sudah ada dalam keranjang belanja.")
                return 
            
        
        if kode_barang in self.data_barang:
            barang = self.data_barang[kode_barang]
            nama_barang = barang["nama_barang"]
            harga_satuan = float(barang["harga"])
            stok = float(barang["stock"])

            if jumlah > stok:
                messagebox.showwarning("Stok Tidak Cukup", f"Stok untuk {nama_barang} tidak mencukupi. Stok tersedia: {stok:.0f}")
                return
            elif jumlah <= 0:
                messagebox.showwarning("Jumlah Tidak Valid", "Jumlah barang harus lebih besar dari 0.")
                return
            total_harga = harga_satuan * jumlah

            self.cart.append({
                "kode": kode_barang,
                "nama": nama_barang,
                "jumlah": jumlah,
                "harga_satuan": harga_satuan,
                "total_harga": total_harga
            })

            self.data_barang[kode_barang]["stock"] = stok - jumlah

            self.save_data()

            self.update_cart_display()
        else:
            messagebox.showerror("Error", "Kode barang tidak ditemukan.")
    def save_data(self):
        import csv
        with open('data_barang.csv', 'w', newline='') as file:
            flie_names = ['kode_barang', 'nama_barang', 'harga', 'stock']
            writer = csv.DictWriter(file, fieldnames=flie_names)
            writer.writeheader()
            for barang in self.data_barang.values():
                writer.writerow({
                    'kode_barang': barang['kode_barang'],
                    'nama_barang': barang['nama_barang'],
                    'harga': barang['harga'],
                    'stock': float(barang['stock'])
                })

    def on_edit_click(self):
        """Fungsi untuk mengedit barang yang dipilih di dalam daftar dengan pop-up."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Silakan pilih item untuk diedit.")
            return

        item = self.tree.item(selected_item[0])
        values = item["values"]
        kode_barang = values[0]

        popup = Toplevel(self.root)
        popup.title("Edit Barang")
        popup.geometry("300x200")
        popup.transient(self.root)
        popup.grab_set()

        Label(popup, text=f"Edit Jumlah untuk {values[1]}", font=("Poppins", 12)).pack(pady=10)

        entry_jumlah = Entry(popup, font=("Poppins", 12), justify="center")
        entry_jumlah.insert(0, str(values[2]))
        entry_jumlah.pack(pady=5)

        def save_edit():
            if not entry_jumlah.get().isdigit():
                messagebox.showerror("Error", "Jumlah harus berupa angka!")
                return

            new_jumlah = int(entry_jumlah.get())
            if new_jumlah <= 0:
                messagebox.showwarning("Jumlah Tidak Valid", "Jumlah barang harus lebih besar dari 0.")
                return
            
            for item in self.cart:
                if item["kode"] == kode_barang:
                    item["jumlah"] = new_jumlah
                    item["total_harga"] = item["harga_satuan"] * new_jumlah
                    item["stock"] = self.data_barang[kode_barang]["stock"] - new_jumlah
                    break

            
            self.save_data()
            self.update_cart_display()
            popup.destroy()

        Button(popup, text="Simpan", font=("Poppins", 12), command=save_edit).pack(pady=10)

    def on_batal_click(self):
        """Menghapus barang yang dipilih dari daftar."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Silakan pilih item untuk dihapus.")
            return

        item = self.tree.item(selected_item[0])
        kode_barang = item["values"][0]

        for item in self.cart:
            if item["kode"] == kode_barang:
                self.data_barang[kode_barang]["stock"] += item["jumlah"]
                break

        self.cart = [item for item in self.cart if item["kode"] != kode_barang]
        self.save_data()
        self.update_cart_display()

    def update_cart_display(self):
        """Memperbarui tampilan daftar barang di Treeview."""
        self.tree.delete(*self.tree.get_children())
        total_price = 0

        for item in self.cart:
            total_price += item["total_harga"]
            self.tree.insert("", "end", values=(
                item["kode"],
                item["nama"],
                item["jumlah"],
                f"Rp {item['harga_satuan']:.0f}",
                f"Rp {item['total_harga']:.0f}"
            ))

        self.total_label.config(text=f"Total: Rp {total_price:.0f}")

    def clear_placeholder(self, entry, placeholder_text):
        """Menghapus placeholder saat Entry difokuskan."""
        if entry.get() == placeholder_text:
            entry.delete(0, "end")
            entry.config(fg="#000000")  # Warna teks hitam

    def add_placeholder(self, entry, placeholder_text):
        """Menambahkan kembali placeholder jika Entry kosong."""
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg="#A0A0A0")  

    def on_selesai_click(self):
        """Melanjutkan ke metode pembayaran."""
        total_price = sum(item["total_harga"] for item in self.cart)
        if total_price == 0:
            messagebox.showinfo("Info", "Keranjang belanja kosong.")
            return

        self.show_payment_popup()

    def show_payment_popup(self):
        """Menampilkan pop-up untuk memilih metode pembayaran."""
        popup = Toplevel(self.root)
        popup.title("Metode Pembayaran")
        popup.geometry("400x400")
        popup.transient(self.root)
        popup.grab_set()

        Label(popup, text="Pilih Metode Pembayaran:", font=("Poppins", 14)).pack(pady=10)

        payment_method = StringVar(value="cash")
        Radiobutton(popup, text="Cash", variable=payment_method, value="cash", font=("Poppins", 12)).pack(pady=5)
        Radiobutton(popup, text="Transfer", variable=payment_method, value="transfer", font=("Poppins", 12)).pack(pady=5)

        def process_payment():
            selected_method = payment_method.get()
            popup.destroy()
            
            if selected_method == "cash":
                self.show_cash_payment_popup()
            elif selected_method == "transfer":
                self.show_qr_code_payment()

        Button(popup, text="Bayar", font=("Poppins", 12), command=process_payment).pack(pady=20)

    def show_loading_animation(self):
        """Menampilkan animasi loading sebelum pembayaran selesai."""
        loading_popup = Toplevel(self.root)
        loading_popup.title("Proses Pembayaran")
        loading_popup.geometry("300x200")
        loading_popup.transient(self.root)
        loading_popup.grab_set()

        Label(loading_popup, text="Memproses pembayaran...", font=("Poppins", 14)).pack(pady=30)

        loading_label = Label(loading_popup, font=("Poppins", 14))
        loading_label.pack()

        def update_loading():
            text = loading_label.cget("text")
            loading_label.config(text=text + "." if len(text) < 10 else "Loading")
            loading_popup.after(300, update_loading)

        update_loading()

        def finish_payment():
            loading_popup.destroy()
            messagebox.showinfo("Berhasil", "Pembayaran berhasil diproses!")

        loading_popup.after(3000, finish_payment)
    def show_cash_payment_popup(self):
        """Menampilkan pop-up untuk pembayaran tunai."""
        popup = Toplevel(self.root)
        popup.title("Pembayaran Tunai")
        popup.geometry("300x200")
        popup.transient(self.root)
        popup.grab_set()

        total_price = sum(item["total_harga"] for item in self.cart)
        Label(popup, text=f"Total: Rp {total_price:.0f}", font=("Poppins", 14)).pack(pady=10)

        Label(popup, text="Masukkan nominal uang:", font=("Poppins", 12)).pack(pady=5)
        entry_nominal = Entry(popup, font=("Poppins", 12), justify="center")
        entry_nominal.pack(pady=5)

        def process_cash():
            nominal = entry_nominal.get()
            if not nominal.isdigit():
                messagebox.showerror("Error", "Nominal harus berupa angka!")
                return

            nominal = int(nominal)
            if nominal < total_price:
                messagebox.showerror("Error", "Uang yang diberikan kurang.")
            else:
                change = nominal - total_price
                popup.destroy()
                messagebox.showinfo("Berhasil", f"Pembayaran berhasil! Kembalian: Rp {change:.0f}")
                self.generate_invoice()

        Button(popup, text="Bayar", font=("Poppins", 12), command=process_cash).pack(pady=20)

    def show_qr_code_payment(self):
        """Menampilkan QR code untuk pembayaran transfer."""
        popup = Toplevel(self.root)
        popup.title("Pembayaran QRIS")
        popup.geometry("300x400")
        popup.transient(self.root)
        popup.grab_set()

        total_price = sum(item["total_harga"] for item in self.cart)
        Label(popup, text=f"Total: Rp {total_price:.0f}", font=("Poppins", 14)).pack(pady=10)

        # Generate QR code
        qr_data = f"Nominal Pembayaran:{total_price}"  
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((200, 200), Image.LANCZOS)  

       
        qr_photo = ImageTk.PhotoImage(qr_img)

        # Create a label to display the QR code
        qr_label = Label(popup, image=qr_photo)
        qr_label.image = qr_photo  
        qr_label.pack(pady=10)

        def confirm_transfer():
            popup.destroy()
            messagebox.showinfo("Berhasil", "Pembayaran berhasil diproses melalui QRIS!")
            self.generate_invoice()

        Button(popup, text="Konfirmasi Pembayaran", font=("Poppins", 12), command=confirm_transfer).pack(pady=20)
    def generate_invoice(self):
        """Membuat file invoice dalam format PDF."""
        if not self.cart:
            messagebox.showinfo("Info", "Keranjang belanja kosong, tidak bisa membuat invoice.")
            return

        # Nama file invoice
        invoice_filename = f"Invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        # Membuat canvas untuk PDF
        c = canvas.Canvas(invoice_filename, pagesize=A4)
        width, height = A4

        # Header Invoice
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, height - 50, "Invoice Pembelian")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Tanggal: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        c.drawString(50, height - 100, "Toko: Mamam Store")
        c.drawString(50, height - 120, "Alamat: Jl. Mulyorejo, Surabaya")

        # Membuat tabel
        y = height - 150
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Kode")
        c.drawString(100, y, "Nama Barang")
        c.drawString(250, y, "Jumlah")
        c.drawString(300, y, "Harga Satuan")
        c.drawString(400, y, "Total")
        y -= 20
        c.setFont("Helvetica", 10)

        total_price = 0
        for item in self.cart:
            c.drawString(50, y, item["kode"])
            c.drawString(100, y, item["nama"])
            c.drawString(250, y, str(item["jumlah"]))
            c.drawString(300, y, f"Rp {item['harga_satuan']:.0f}")
            c.drawString(400, y, f"Rp {item['total_harga']:.0f}")
            total_price += item["total_harga"]
            y -= 20

        # Total pembayaran
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y - 20, f"Total Pembayaran: Rp {total_price:.0f}")

        # Footer
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(50, y - 60, "Terima kasih telah berbelanja di Toko Kami!")
        c.drawString(50, y - 80, "Harap simpan invoice ini sebagai bukti pembayaran.")

        # Simpan file PDF
        c.save()

        # Tampilkan notifikasi
        messagebox.showinfo("Invoice Dibuat", f"Invoice berhasil dibuat: {invoice_filename}")
    def show_invoice_button(self):
        """Menampilkan tombol Cetak Invoice setelah pembayaran selesai."""
        invoice_button = Button(
            self.root,
            text="Cetak Invoice",
            font=("Poppins", 12),
            bg="#4CAF50",
            fg="white",
            command=self.generate_invoice
        )
        invoice_button.place(x=450, y=650, width=120, height=40)


# Main program
if __name__ == "__main__":
    root = Tk()
    app = PelangganApp(root)
    root.mainloop()
