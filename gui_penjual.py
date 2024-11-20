from pathlib import Path # untuk memanggil file csv, berdasarkan direktori file
from tkinter import Tk, Canvas, Button, PhotoImage, Scrollbar, Frame, messagebox, Toplevel, Checkbutton, BooleanVar, Label
import csv # untuk membaca dan menulis file csv
from gui_edit_barang import EditBarangApp # untuk memanggil file gui_edit_barang
from gui_add_barang import TambahBarangApp # untuk memanggil file gui_add_barang
class KasirManagerApp: # ini untuk class KasirManagerApp
    def __init__(self, root): # nah ini untuk fungsi __init__ yaitu untuk inisialisasi aplikasi dalam class KasirManagerApp
        self.root = root
        self.root.geometry("1024x720")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.selected_items = {}  # Dictionary untuk menyimpan item yang dipilih
        self.checkboxes = {}      # Dictionary untuk menyimpan checkbox widgets

        self.output_path = Path(__file__).parent # untuk memanggil direktori file
        self.assets_path = self.output_path / Path("E:\\UTS_PEMKOM\\build\\assets\\frame2") 
        self.barang_csv_path = self.output_path / "data_barang.csv" 

        self.setup_canvas() # untuk memanggil fungsi setup_canvas dalam class KasirManagerApp 
        self.load_assets() # untuk memanggil fungsi load_assets dalam class KasirManagerApp
        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path: # untuk memanggil direktori file
        return self.assets_path / Path(path)

    def setup_canvas(self): 
        self.canvas = Canvas(self.root, bg="#FFFFFF", height=720, width=1024, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

    def load_assets(self):
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))

    def setup_ui(self): # untuk memanggil fungsi setup_ui dalam class KasirManagerApp
        self.canvas.create_image(512.0, 384.0, image=self.image_1)
        self.canvas.create_image(512.0, 686.0, image=self.image_2)

        self.canvas.create_text(112.0, 74.0, anchor="nw", text="Hallo, User", fill="#FFFFF2", font=("Poppins ExtraBold", 48 * -1))
        self.canvas.create_text(287.0, 176.0, anchor="nw", text="Silahkan Manage Stok Barang Anda!", fill="#FFFFF2", font=("Poppins SemiBold", 24 * -1))

        self.button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.on_add_item, relief="flat")
        self.button_1.place(x=257.0, y=578.0, width=145.0, height=47.0)

        self.button_2 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.on_edit_item, relief="flat")
        self.button_2.place(x=440.0, y=578.0, width=145.0, height=47.0)

        self.button_3 = Button(image=self.button_image_3, borderwidth=0, highlightthickness=0, command=self.on_delete_item, relief="flat")
        self.button_3.place(x=623.0, y=578.0, width=145.0, height=47.0)

        self.create_scrollable_table() # nah ini untuk memanggil fungsi create_scrollable_table
        self.button_back = Button(
            text="Kembali",
            font=("Poppins", 14),
            bg="#FFDDC1",
            fg="#000000",
            borderwidth=0,
            highlightthickness=0,
            command=self.on_back_button,
            relief="flat"
        )
        self.button_back.place(x=806.0, y=578.0, width=145.0, height=47.0)


    def create_scrollable_table(self): # nah ini untuk fungsi create_scrollable_table
        self.table_frame = Frame(self.canvas, bg="#FFFFFF")
        self.table_frame.place(x=116.0, y=311.0, width=790.0, height=200.0)

        
        self.scrollbar = Scrollbar(self.table_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.table = Canvas(self.table_frame, bg="#FFFFFF", highlightthickness=0)
        self.table.pack(side="left", fill="both", expand=True)

        
        self.inner_frame = Frame(self.table, bg="#FFFFFF")
        self.table.create_window((0, 0), window=self.inner_frame, anchor="nw")

        
        self.scrollbar.config(command=self.table.yview)
        self.table.config(yscrollcommand=self.scrollbar.set)

        
        self.table.bind_all("<MouseWheel>", self._on_mouse_scroll)
        
        
        self.read_data_barang()

        
        self.inner_frame.update_idletasks() # ini untuk mengupdate idletasks dari inner_frame
        self.table.config(scrollregion=self.table.bbox("all"))

    def _on_mouse_scroll(self, event): # nah ini untuk fungsi _on_mouse_scroll
        self.table.yview_scroll(-1 * (event.delta // 120), "units")

    def read_data_barang(self):
        
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.selected_items.clear()
        self.checkboxes.clear()

        # Create headers
        headers = ["", "No", "Kode Barang", "Nama Barang", "Stok", "Harga"] # nah ini untuk membuat header
        
        # Create header row
        for i, header in enumerate(headers): # nah ini untuk membuat header
            Label(self.inner_frame, text=header, bg="#FFFFFF", font=("Poppins", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)
            
        try:
            with open(self.barang_csv_path, mode="r") as file: # nah ini untuk membuka file csv
                reader = list(csv.DictReader(file))
                for idx, row in enumerate(reader, start=1):
                    # Create checkbox
                    var = BooleanVar()
                    self.selected_items[idx] = {"var": var, "data": row}
                    
                    # Add checkbox
                    checkbox = Checkbutton(self.inner_frame, variable=var, bg="#FFFFFF")
                    checkbox.grid(row=idx, column=0, padx=5)
                    
                    # Add data labels
                    Label(self.inner_frame, text=str(idx), bg="#FFFFFF").grid(row=idx, column=1, padx=5)
                    Label(self.inner_frame, text=row["kode_barang"], bg="#FFFFFF").grid(row=idx, column=2, padx=5)
                    Label(self.inner_frame, text=row["nama_barang"], bg="#FFFFFF").grid(row=idx, column=3, padx=5)
                    Label(self.inner_frame, text=int(float(row["stock"])), bg="#FFFFFF").grid(row=idx, column=4, padx=5)  # Ubah stok menjadi int
                    Label(self.inner_frame, text=f"Rp {int(float(row['harga'])):,}", bg="#FFFFFF").grid(row=idx, column=5, padx=5)  # Format harga

        except Exception as e:
            messagebox.showerror("Error", f"Error saat membaca data: {str(e)}")
            
    def get_selected_items(self):
        """Return list of selected items"""
        return [data["data"] for idx, data in self.selected_items.items() if data["var"].get()]
    def on_back_button(self):
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin kembali?")
        if confirm:
            from LandingPage3 import KasirApp
            self.root.destroy()  
            
            main_root = Tk()  
            KasirApp(main_root)

            main_root.mainloop()

    def on_add_item(self):
        TambahBarangApp(self.root)
    def on_edit_item(self):
        selected = self.get_selected_items()
        if not selected:
            messagebox.showwarning("Pilih Barang", "Pilih barang terlebih dahulu untuk diedit.")
        elif len(selected) > 1:
            messagebox.showwarning("Terlalu Banyak", "Pilih hanya satu barang untuk diedit.")
        else:
            item_to_edit = selected[0]
            self.open_edit_item_window(item_to_edit)

    def open_edit_item_window(self, item_to_edit): # nah ini untuk fungsi open_edit_item_window
        # Tutup jendela utama
        self.root.destroy()
        
        # Buka jendela EditBarangApp
        edit_root = Tk()
        edit_app = EditBarangApp(edit_root)
        edit_app.current_barang = item_to_edit["kode_barang"]  
        edit_root.mainloop()

    def on_delete_item(self): # nah ini untuk fungsi on_delete_item
        selected = self.get_selected_items()
        if not selected:
            messagebox.showwarning("Pilih Barang", "Pilih barang yang ingin dihapus.")
            return

        items_text = "\n".join([item['nama_barang'] for item in selected]) # nah ini untuk membuat items_text
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus barang berikut?\n{items_text}")
        
        if confirm:
            try:
                with open(self.barang_csv_path, mode="r") as file: # nah ini untuk membuka file csv
                    reader = list(csv.DictReader(file))
                
                
                updated_data = [row for row in reader if row not in selected]

                with open(self.barang_csv_path, mode="w", newline="") as file: # nah ini untuk membuka file csv
                    writer = csv.DictWriter(file, fieldnames=["kode_barang", "nama_barang", "stock", "harga"])
                    writer.writeheader()
                    writer.writerows(updated_data)

                messagebox.showinfo("Sukses", "Barang berhasil dihapus.") # nah ini untuk menampilkan pesan sukses
                self.read_data_barang()
            except Exception as e:
                messagebox.showerror("Error", f"Error saat menghapus barang: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = KasirManagerApp(root)
    root.mainloop()