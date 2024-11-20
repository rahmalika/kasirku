import csv
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Checkbutton, BooleanVar, messagebox
from gui_penjual import KasirManagerApp
class LoginApp:
    def __init__(self, root, prev_window=None):
        self.root = root
        self.prev_window = prev_window  # Menyimpan referensi ke jendela sebelumnya
        self.root.geometry("1024x720")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"E:\UTS_PEMKOM\build\assets\frame1")
        self.csv_path = self.output_path / "data_users.csv"  

        self.setup_canvas()
        self.load_assets()
        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        """Helper function to get the path of assets."""
        return self.assets_path / Path(path)

    def setup_canvas(self):
        """Setup the main canvas."""
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

    def load_assets(self):
        """Load assets like images and buttons."""
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))  # Button Kembali
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))  # Button Login
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))

    def setup_ui(self):
        """Setup UI elements."""
        # Background image
        self.canvas.create_image(
            512.0,
            384.0,
            image=self.image_1
        )

        # Text labels
        self.canvas.create_text(
            112.0,
            74.0,
            anchor="nw",
            text="SELAMAT DATANG DI KASIRKU",
            fill="#FFFFF2",
            font=("Poppins ExtraBold", 48 * -1)
        )
        self.canvas.create_text(
            287.0,
            176.0,
            anchor="nw",
            text="Silahkan Masukkan Username dan Password Anda!",
            fill="#FFFFF2",
            font=("Poppins SemiBold", 24 * -1)
        )

        # Footer image
        self.canvas.create_image(
            512.0,
            686.0,
            image=self.image_2
        )

        # Entry fields
        self.entry_bg_1 = self.canvas.create_image(
            512.0,
            351.0,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=312.0,
            y=324.0,
            width=400.0,
            height=52.0
        )

        self.entry_bg_2 = self.canvas.create_image(
            512.0,
            450.0,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            show="*"  # Menambahkan masking untuk password (bintang-bintang)
        )
        self.entry_2.place(
            x=312.0,
            y=423.0,
            width=400.0,
            height=52.0
        )

        # Checkbox untuk menampilkan/menghapus password
        self.show_password_var = BooleanVar()
        self.show_password_checkbox = Checkbutton(
            self.root,
            text="Tampilkan Password",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            bg="#FFFFFF",
            font=("Poppins", 14)
        )
        # Mengubah posisi checkbox untuk berada di bawah input password
        self.show_password_checkbox.place(x=312.0, y=485.0)

        # Buttons
        self.button_1 = Button(
            image=self.button_image_1,  # Button Kembali
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_1_click,  # Fungsi untuk Kembali
            relief="flat"
        )
        self.button_1.place(
            x=1.0,
            y=572.0,
            width=182.0,
            height=53.0
        )

        self.button_2 = Button(
            image=self.button_image_2,  # Button Login
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_2_click,  # Fungsi untuk Login
            relief="flat"
        )
        self.button_2.place(
            x=842.0,
            y=581.0,
            width=182.0,
            height=53.0
        )
        self.add_placeholder(self.entry_1, "Masukkan Username Anda")  
        self.add_placeholder(self.entry_2, "Password")  

    def toggle_password_visibility(self):
        """Fungsi untuk menampilkan atau menyembunyikan password berdasarkan checkbox."""
        if self.show_password_var.get():
            self.entry_2.config(show="")  
        else:
            self.entry_2.config(show="*")  
    def on_button_1_click(self):
        """Handle button 1 click event (Kembali)."""
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin kembali?")
        if confirm:
            self.root.destroy()
            from LandingPage3 import KasirApp
            main_root = Tk()  
            KasirApp(main_root) 
            main_root.mainloop()
            

    def on_button_2_click(self):
        """Handle button 2 click event (Login)."""
        username = self.entry_1.get().strip()
        password = self.entry_2.get().strip()

        if self.validate_login(username, password):
            messagebox.showinfo("Login Berhasil", "Selamat Datang!")
            self.root.destroy()  # Menutup jendela login

            # Membuka KasirManagerApp
            new_window = Tk()
            app = KasirManagerApp(new_window)
            new_window.mainloop()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!\nSilahkan coba lagi.")

    def validate_login(self, username, password):
        """Validate login credentials from CSV."""
        try:
            with open(self.csv_path, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["username"] == username and row["password"] == password:
                        return True
        except FileNotFoundError:
            messagebox.showerror("File Error", "File users.csv tidak ditemukan!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
        return False
    def add_placeholder(self, entry_widget, placeholder_text):
        """
        Menambahkan placeholder pada widget Entry.
        """
        entry_widget.insert(0, placeholder_text)
        entry_widget.config(fg="grey")  # Ubah warna teks untuk membedakan placeholder

        def on_focus_in(event):
            if entry_widget.get() == placeholder_text:
                entry_widget.delete(0, "end")
                entry_widget.config(fg="black")  # Ubah warna teks menjadi normal

        def on_focus_out(event):
            if not entry_widget.get():
                entry_widget.insert(0, placeholder_text)
                entry_widget.config(fg="grey")  # Kembali ke placeholder

        # Bind event focus in dan out
        entry_widget.bind("<FocusIn>", on_focus_in)
        entry_widget.bind("<FocusOut>", on_focus_out)



if __name__ == "__main__":
    root = Tk()
    app = LoginApp(root)
    root.mainloop()
