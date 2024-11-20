from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Scrollbar, Frame, messagebox, Toplevel, Checkbutton, BooleanVar, Label
import csv

class KasirManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x720")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.selected_items = {}  # Dictionary untuk menyimpan item yang dipilih
        self.checkboxes = {}      # Dictionary untuk menyimpan checkbox widgets

        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path("E:\\UTS_PEMKOM\\build\\assets\\frame2")
        self.barang_csv_path = self.output_path / "data_barang.csv"

        self.setup_canvas()
        self.load_assets()
        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
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

    def setup_ui(self):
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

        self.create_scrollable_table()

    def create_scrollable_table(self):
        self.table_frame = Frame(self.canvas, bg="#FFFFFF")
        self.table_frame.place(x=116.0, y=311.0, width=790.0, height=200.0)

        # Create canvas and scrollbar
        self.scrollbar = Scrollbar(self.table_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.table = Canvas(self.table_frame, bg="#FFFFFF", highlightthickness=0)
        self.table.pack(side="left", fill="both", expand=True)

        # Create frame inside canvas for widgets
        self.inner_frame = Frame(self.table, bg="#FFFFFF")
        self.table.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Configure scrollbar
        self.scrollbar.config(command=self.table.yview)
        self.table.config(yscrollcommand=self.scrollbar.set)

        # Bind mouse wheel
        self.table.bind_all("<MouseWheel>", self._on_mouse_scroll)
        
        # Load data
        self.read_data_barang()

        # Update scroll region
        self.inner_frame.update_idletasks()
        self.table.config(scrollregion=self.table.bbox("all"))

    def _on_mouse_scroll(self, event):
        self.table.yview_scroll(-1 * (event.delta // 120), "units")

    def read_data_barang(self):
        # Clear existing widgets
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.selected_items.clear()
        self.checkboxes.clear()

        # Create headers
        headers = ["", "No", "Kode Barang", "Nama Barang", "Stok", "Harga"]
        
        # Create header row
        for i, header in enumerate(headers):
            Label(self.inner_frame, text=header, bg="#FFFFFF", font=("Poppins", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)
            
        try:
            with open(self.barang_csv_path, mode="r") as file:
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
                    Label(self.inner_frame, text=row["stock"], bg="#FFFFFF").grid(row=idx, column=4, padx=5)
                    Label(self.inner_frame, text=row["harga"], bg="#FFFFFF").grid(row=idx, column=5, padx=5)

        except Exception as e:
            messagebox.showerror("Error", f"Error saat membaca data: {str(e)}")

    def get_selected_items(self):
        """Return list of selected items"""
        return [data["data"] for idx, data in self.selected_items.items() if data["var"].get()]

    def on_add_item(self):
        messagebox.showinfo("Tambah Barang", "Fungsi untuk menambah barang belum ditambahkan.")

    def on_edit_item(self):
        selected = self.get_selected_items()
        if not selected:
            messagebox.showwarning("Pilih Barang", "Pilih barang terlebih dahulu untuk diedit.")
        elif len(selected) > 1:
            messagebox.showwarning("Terlalu Banyak", "Pilih hanya satu barang untuk diedit.")
        else:
            messagebox.showinfo("Edit Barang", f"Fitur Edit Barang untuk: {selected[0]['nama_barang']}.")

    def on_delete_item(self):
        selected = self.get_selected_items()
        if not selected:
            messagebox.showwarning("Pilih Barang", "Pilih barang yang ingin dihapus.")
            return

        items_text = "\n".join([item['nama_barang'] for item in selected])
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus barang berikut?\n{items_text}")
        
        if confirm:
            try:
                with open(self.barang_csv_path, mode="r") as file:
                    reader = list(csv.DictReader(file))
                
                # Filter out selected items
                updated_data = [row for row in reader if row not in selected]

                with open(self.barang_csv_path, mode="w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["kode_barang", "nama_barang", "stock", "harga"])
                    writer.writeheader()
                    writer.writerows(updated_data)

                messagebox.showinfo("Sukses", "Barang berhasil dihapus.")
                self.read_data_barang()
            except Exception as e:
                messagebox.showerror("Error", f"Error saat menghapus barang: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = KasirManagerApp(root)
    root.mainloop()