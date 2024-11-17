
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Project\Coding\Tugas Zilka\UI Kasir\build\assets\frame5")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1024x720")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1024,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    512.0,
    384.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    512.0,
    686.0,
    image=image_image_2
)

canvas.create_text(
    112.0,
    41.0,
    anchor="nw",
    text="Invoice Belanja",
    fill="#FFFFF2",
    font=("Poppins ExtraBold", 48 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=440.0,
    y=565.0,
    width=145.0,
    height=47.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=626.0,
    y=565.0,
    width=196.0,
    height=47.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=228.0,
    y=565.0,
    width=145.0,
    height=47.0
)

canvas.create_text(
    91.0,
    203.0,
    anchor="nw",
    text="No Invoice",
    fill="#FFFFF2",
    font=("Poppins SemiBold", 24 * -1)
)

canvas.create_text(
    112.0,
    261.0,
    anchor="nw",
    text="Nama Barang",
    fill="#FFFFF2",
    font=("Poppins SemiBold", 24 * -1)
)

canvas.create_text(
    573.0,
    261.0,
    anchor="nw",
    text="Qty",
    fill="#FFFFF2",
    font=("Poppins SemiBold", 24 * -1)
)

canvas.create_text(
    768.0,
    253.0,
    anchor="nw",
    text="Harga",
    fill="#FFFFF2",
    font=("Poppins SemiBold", 24 * -1)
)
window.resizable(False, False)
window.mainloop()