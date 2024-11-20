import pandas as pd
import uuid
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox

class EditBarangApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x720")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)
        self.root.title("Edit Barang")
        self.current_barang = None

        self.ASSETS_PATH = Path(r"E:\\UTS_PEMKOM\\build\\assets\\frame6")
        self.image_refs = []  # List untuk menyimpan referensi gambar
        self.setup_ui()

        # Path file CSV
        self.csv_file = Path("data_barang.csv")  # Menggunakan nama file yang sesuai

        # Barang yang sedang diedit (default None)
        self.current_barang = None  

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
            text="Halaman Edit Barang",
            fill="#FFFFF2",
            font=("Poppins ExtraBold", 48 * -1)
        )
        self.canvas.create_text(
            287.0, 176.0, anchor="nw",
            text="Edit data barang dengan nilai yang valid",
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

        # Panggil fungsi untuk load data barang yang akan diedit
        self.load_item_data()

    def add_image(self, file_name, x, y):
        image = PhotoImage(file=self.relative_to_assets(file_name))
        self.image_refs.append(image)  # Simpan referensi gambar
        self.canvas.create_image(x, y, image=image)

    def create_input_field(self, x, y, image_file, width, height, placeholder=""):
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

    def on_focus_in(self, event, entry, placeholder):
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

    def load_item_data(self):
        try:
            if self.current_barang:
                # Load data dari file CSV
                if not self.csv_file.exists():
                    messagebox.showerror("Error", "File data barang tidak ditemukan!")
                    return

                df = pd.read_csv(self.csv_file)
                item_data = df.loc[df['kode_barang'] == self.current_barang]

                if item_data.empty:
                    messagebox.showerror("Error", "Data barang tidak ditemukan!")
                    return

                # Ambil data barang yang akan diedit
                nama_barang = item_data['nama_barang'].values[0]
                harga_barang = str(item_data['harga'].values[0])
                jumlah_barang = str(item_data['stock'].values[0])

                # Atur placeholder sesuai data barang
                self.setup_input_field_placeholder(self.entry_1, nama_barang)
                self.setup_input_field_placeholder(self.entry_2, harga_barang)
                self.setup_input_field_placeholder(self.entry_3, jumlah_barang)

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memuat data barang: {str(e)}")


    def setup_input_field_placeholder(self, entry, placeholder):
        """Mengatur placeholder untuk field input."""
        entry.delete(0, "end")
        entry.insert(0, placeholder)
        entry.config(fg="#A9A9A9")  # Warna placeholder abu-abu

        entry.bind("<FocusIn>", lambda event, e=entry, p=placeholder: self.on_focus_in(event, e, p))
        entry.bind("<FocusOut>", lambda event, e=entry, p=placeholder: self.on_focus_out(event, e, p))

    def on_button_1_click(self):
        # Get data from input fields
        nama_barang = self.entry_1.get().strip()
        harga_barang = self.entry_2.get().strip()
        jumlah_barang = self.entry_3.get().strip()

        # Validate input fields
        if not nama_barang or not harga_barang or not jumlah_barang:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        try:
            # Convert harga_barang and jumlah_barang to integers
            harga_barang = int(harga_barang)
            jumlah_barang = int(jumlah_barang)

            # Update data barang
            self.edit_barang(nama_barang, harga_barang, jumlah_barang)

        except ValueError:
            messagebox.showerror("Error", "Harga dan jumlah harus berupa angka yang valid!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def edit_barang(self, nama_barang, harga_barang, jumlah_barang):
        try:
            # Load data dari file CSV
            if not self.csv_file.exists():
                messagebox.showerror("Error", "File data barang tidak ditemukan!")
                return

            df = pd.read_csv(self.csv_file)

            # Pastikan barang yang akan diedit ada dalam data
            if self.current_barang not in df['kode_barang'].values:
                messagebox.showerror("Error", "Barang tidak ditemukan!")
                return

            # Update data barang
            df.loc[df['kode_barang'] == self.current_barang, ['nama_barang', 'stock', 'harga']] = [nama_barang, jumlah_barang, harga_barang]

            # Simpan perubahan ke file CSV
            df.to_csv(self.csv_file, index=False)

            messagebox.showinfo("Sukses", f"Barang berhasil diperbarui!")
            self.root.destroy()
            self.run_previous_page()

        except Exception as e:
            messagebox.showerror("Gagal", f"Gagal memperbarui barang. Kesalahan: {str(e)}")

    def on_button_2_click(self):
        self.root.destroy()
        self.run_previous_page()

    def run_previous_page(self):
        from gui_penjual import KasirManagerApp
        previous_root = Tk()
        KasirManagerApp(previous_root)
        previous_root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = EditBarangApp(root)
    root.mainloop()
