import tkinter as tk
from tkinter import CENTER

def halaman_pembeli(window_landing_page, landing_page):
    # Menghapus konten lama
    for widget in window_landing_page.winfo_children():
        widget.destroy()
    
    # Menampilkan teks dan tombol kembali
    text = tk.Label(window_landing_page, text="Halaman Pembeli", bg="#23C9FF", fg="white", font=("Poppins", 30))
    text.pack(pady=50)

    tombol_kembali = tk.Button(window_landing_page, text="Kembali", command=landing_page, font=("Arial", 14), bg="#3bdfff", fg="black", width=10, height=2)
    tombol_kembali.place(relx=0.5, rely=0.6, anchor=CENTER)
