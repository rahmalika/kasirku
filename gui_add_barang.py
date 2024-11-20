import pandas as pd
import uuid # nah ini untuk kode unik
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
class TambahBarangApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x720")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.ASSETS_PATH = Path(r"E:\\UTS_PEMKOM\\build\\assets\\frame3") # nah ini pathnya lokasi folder assets
        self.image_refs = []  # List untuk menyimpan referensi gambar
        self.setup_ui()

        # Path file CSV
        self.csv_file = Path("data_barang.csv")  # Menggunakan nama file yang sesuai

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def setup_ui(self):
        # Canvas setup
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

        # Background images
        self.add_image("image_1.png", 512.0, 384.0)
        self.add_image("image_2.png", 512.0, 686.0)

        # Text elements
        self.canvas.create_text(
            112.0, 74.0, anchor="nw",
            text="Halaman Tambah Barang",
            fill="#FFFFF2",
            font=("Poppins ExtraBold", 48 * -1)
        )
        self.canvas.create_text(
            287.0, 176.0, anchor="nw",
            text="Silahkan data barang dengan nilai yang valid",
            fill="#FFFFF2",
            font=("Poppins SemiBold", 24 * -1)
        )

        # Input fields dengan placeholder
        self.entry_1 = self.create_input_field(130.0, 261.0, "entry_1.png", 765.0, 55.0, placeholder="Nama Barang")
        self.entry_2 = self.create_input_field(129.0, 356.0, "entry_2.png", 765.0, 55.0, placeholder="Harga Barang")
        self.entry_3 = self.create_input_field(131.0, 451.0, "entry_3.png", 765.0, 55.0, placeholder="Jumlah Barang")

        # Buttons
        self.create_button(116.0, 556.0, "button_1.png", 145.0, 47.0, self.on_button_1_click)
        self.create_button(767.0, 546.0, "button_2.png", 145.0, 47.0, self.on_button_2_click)

    def add_image(self, file_name, x, y): # nah ini fungsi untuk menambahkan gambar
        image = PhotoImage(file=self.relative_to_assets(file_name))
        self.image_refs.append(image)  # Simpan referensi gambar
        self.canvas.create_image(x, y, image=image)

    def create_input_field(self, x, y, image_file, width, height, placeholder=""): # nah ini fungsi untuk membuat field input
        entry_image = PhotoImage(file=self.relative_to_assets(image_file))
        self.image_refs.append(entry_image)  # Simpan referensi gambar
        self.canvas.create_image(x + width / 2, y + height / 2, image=entry_image)
        
        # Create the Entry widget with placeholder and centered text
        entry = Entry(self.root, bd=0, bg="#FFFFFF", fg="#A9A9A9", font=("Poppins", 14), highlightthickness=0, justify="center")
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, placeholder)  # Set placeholder text
        entry.bind("<FocusIn>", lambda event, e=entry, p=placeholder: self.on_focus_in(event, e, p))
        entry.bind("<FocusOut>", lambda event, e=entry, p=placeholder: self.on_focus_out(event, e, p))
        
        return entry  # Return the entry widget

    def on_focus_in(self, event, entry, placeholder): # nah ini fungsi untuk mengatur placeholder ket us pw
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="#000716")  # Set font color to black on focus

    def on_focus_out(self, event, entry, placeholder):
        if not entry.get().strip():
            entry.insert(0, placeholder)
            entry.config(fg="#A9A9A9")  # Set font color to gray when unfocused

    def create_button(self, x, y, image_file, width, height, command):
        button_image = PhotoImage(file=self.relative_to_assets(image_file))
        self.image_refs.append(button_image)  # Simpan referensi gambar
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        button.place(x=x, y=y, width=width, height=height)
        setattr(self, f"{image_file}_button", button)

    def on_button_1_click(self):
        # Get data from input fields
        nama_barang = self.entry_1.get().strip()  # Access directly from entry_1
        harga_barang = self.entry_2.get().strip()  # Access directly from entry_2
        jumlah_barang = self.entry_3.get().strip()  # Access directly from entry_3

        # Validate input fields
        if not nama_barang or not harga_barang or not jumlah_barang:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
        if harga_barang == "0" or jumlah_barang == "0":
            messagebox.showerror("Error", "Harga dan jumlah barang tidak boleh 0!")
            return

        try:
            # Convert harga_barang and jumlah_barang to integers
            harga_barang = int(harga_barang)  # Menggunakan float untuk harga
            jumlah_barang = int(jumlah_barang)  # Menggunakan float untuk jumlah

            # Generate a unique item code (UUID-based)
            kode_barang = self.generate_unique_code()

            # Try to save to CSV
            self.tambah_barang(kode_barang, nama_barang, harga_barang, jumlah_barang)

        except ValueError: # ini untuk mengindentifikasi error
            # If conversion to float fails
            messagebox.showerror("Error", "Harga dan jumlah harus berupa angka yang valid!")
        except Exception as e: 
            # If there is any other error
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def on_button_2_click(self):
        print("Button 2 clicked")
        from gui_penjual import KasirManagerApp
        KasirManagerApp(self.root)

    def generate_unique_code(self): # nah ini untuk kode unik barangnya
        """Generate a unique code for the item (5 characters from UUID)."""
        unique_code = str(uuid.uuid4()).replace("-", "")[:5].upper()
        return unique_code

    def tambah_barang(self, kode_barang, nama_barang, harga_barang, jumlah_barang):
        try:
            # Memuat data dari file CSV jika file sudah ada
            if self.csv_file.exists():
                df = pd.read_csv(self.csv_file)
            else:
                df = pd.DataFrame(columns=["kode_barang", "nama_barang", "stock", "harga"])

            # Membuat DataFrame baru untuk entri yang akan ditambahkan
            new_entry = pd.DataFrame([[kode_barang, nama_barang, harga_barang, jumlah_barang]], columns=df.columns)

            # Menghapus baris yang hanya berisi nilai NA, jika ada
            new_entry = new_entry.dropna(how='all')

            # Pastikan `new_entry` tidak kosong sebelum `concat`
            if not new_entry.empty:
                df = pd.concat([df, new_entry], ignore_index=True)

            # Menyimpan kembali ke file CSV
            df.to_csv(self.csv_file, index=False) # ini buat simpan ke file

            messagebox.showinfo("Sukses", f"Barang '{nama_barang}' dengan Kode '{kode_barang}' berhasil ditambahkan!")
            self.entry_1.delete(0, "end")
            self.entry_2.delete(0, "end")
            self.entry_3.delete(0, "end")
            self.root.destroy()
            self.run_previous_page()

        except Exception as e:
            messagebox.showerror("Gagal", f"Gagal menambahkan barang. Kesalahan: {str(e)}")

    def run_previous_page(self): # buat kembali ke halaman sebelumnya
        previous_root = Tk()
        from gui_penjual import KasirManagerApp
        previous_app = KasirManagerApp(previous_root)
        previous_root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = TambahBarangApp(root)
    root.mainloop()
