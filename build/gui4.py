
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Project\Coding\Tugas Zilka\UI Kasir\build\assets\frame4")


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
    144.0,
    40.0,
    anchor="nw",
    text="Hallo, Pelanggan yang baik!",
    fill="#FFFFF2",
    font=("Poppins ExtraBold", 48 * -1)
)

canvas.create_text(
    286.0,
    144.0,
    anchor="nw",
    text="silahkan masukkan kode barang dan jumlah yang kamu beli",
    fill="#FFFFF2",
    font=("Poppins SemiBold", 24 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    234.31764221191406,
    260.5,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=106.0,
    y=243.0,
    width=256.6352844238281,
    height=33.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    449.0,
    260.5,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=373.0,
    y=243.0,
    width=152.0,
    height=33.0
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
    x=116.0,
    y=556.0,
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
    x=525.0,
    y=556.0,
    width=145.0,
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
    x=748.0,
    y=556.0,
    width=145.0,
    height=47.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=325.0,
    y=556.0,
    width=145.0,
    height=47.0
)

canvas.create_rectangle(
    100.0,
    305.0,
    963.6318969726562,
    527.0,
    fill="#FFFFFF",
    outline="")
window.resizable(False, False)
window.mainloop()
