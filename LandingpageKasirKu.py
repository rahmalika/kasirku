import tkinter as tk
from tkinter import CENTER
from Pembeli import halaman_pembeli  
from Penjual import halaman_penjual  
# from Penjual import label_nama_barang

def landing_page():
    for widget in window_landing_page.winfo_children():
        widget.destroy()
    
# Cover KasirKu
    text = tk.Label(window_landing_page, text="Selamat Datang di KasirKu!", bg="#23C9FF", fg="white", font=("Poppins", 30))
    text.pack(pady=50)

# Halaman Pembeli
    tombol_pembeli_button = tk.Button(window_landing_page, text="Pembeli", command=lambda: halaman_pembeli(window_landing_page, landing_page), font=("Arial", 14), bg="#3bdfff", fg="black", width=10, height=2)
    tombol_pembeli_button.place(relx=0.25, rely=0.6, anchor=CENTER)

# Halaman Penjual
    tombol_penjual_button = tk.Button(window_landing_page, text="Penjual", command=lambda: halaman_penjual(window_landing_page, landing_page), font=("Arial", 14), bg="#3bdfff", fg="black", width=10, height=2)
    tombol_penjual_button.place(relx=0.75, rely=0.6, anchor=CENTER)

    
root = tk.Tk()
root.withdraw()  

window_landing_page = tk.Toplevel(root)
window_landing_page.wm_title("KasirKu")
window_landing_page['background'] = "#23C9FF"
window_landing_page.geometry("1080x720")

landing_page()

root.mainloop()
