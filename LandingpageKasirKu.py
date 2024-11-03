import tkinter as tk
from tkinter import CENTER
import tkinter.messagebox as msg
from Pembeli import halaman_pembeli  
from Penjual import halaman_penjual  

def landing_page():
    for widget in window_landing_page.winfo_children():
        widget.destroy()
    
    # Teks Selamat Datang
    text = tk.Label(window_landing_page, text="Selamat Datang di\nKasirKu", bg="#f9f5e7", fg="black", font=("Poppins", 36, "bold"))
    text.pack(pady=(60, 10))

    # Subjudul
    subtext = tk.Label(window_landing_page, text="Pembayaran Mudah dalam Genggaman Anda!", bg="#f9f5e7", fg="black", font=("Poppins", 16))
    subtext.pack(pady=(0, 20))

    # Frame untuk Tombol
    button_frame = tk.Frame(window_landing_page, bg="#f9f5e7")
    button_frame.pack(pady=(0, 40))

    # Tombol Penjual dan Pembeli dalam Frame
    tombol_penjual_button_left = tk.Button(button_frame, text="Penjual", command=lambda: halaman_penjual(window_landing_page, landing_page), font=("Arial", 14), bg="#3bdfff", fg="black", width=10, height=2)
    tombol_penjual_button_left.grid(row=0, column=0, padx=10)

    tombol_penjual_button_right = tk.Button(button_frame, text="Pembeli", command=lambda: halaman_pembeli(window_landing_page, landing_page), font=("Arial", 14), bg="#3bdfff", fg="black", width=10, height=2)
    tombol_penjual_button_right.grid(row=0, column=1, padx=10)

    # Footer
    footer = tk.Label(window_landing_page, text="©2024 | Rahmalika Aumara Zilka 165231005", bg="#3bdfff", fg="black", font=("Poppins", 10))
    footer.pack(side="bottom", fill="x", pady=10)

# Pengaturan Jendela Utama
root = tk.Tk()
root.withdraw()  

window_landing_page = tk.Toplevel(root)
window_landing_page.wm_title("KasirKu")
window_landing_page['background'] = "#f9f5e7"  # Warna background lebih terang sesuai gambar
window_landing_page.geometry("720x480")

def on_closing():
    if msg.askokcancel("Keluar", "Apakah Anda yakin ingin keluar?"):
        window_landing_page.destroy()
        root.destroy()

window_landing_page.protocol("WM_DELETE_WINDOW", on_closing)

landing_page()

root.mainloop()
