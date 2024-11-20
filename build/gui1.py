from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage

class KasirApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x720")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        # Define paths
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"E:\UTS_PEMKOM\build\assets\frame1")

        # Initialize UI
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
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
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
            text="Silahkan Masukkan Usename dan Password Anda!",
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
        self.entry_1 = Text(
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
        self.entry_2 = Text(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.place(
            x=312.0,
            y=423.0,
            width=400.0,
            height=52.0
        )

        # Buttons
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_1_click,
            relief="flat"
        )
        self.button_1.place(
            x=1.0,
            y=572.0,
            width=182.0,
            height=53.0
        )

        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button_2_click,
            relief="flat"
        )
        self.button_2.place(
            x=842.0,
            y=581.0,
            width=182.0,
            height=53.0
        )

    def on_button_1_click(self):
        """Handle button 1 click event."""
        print("Button 1 clicked")

    def on_button_2_click(self):
        """Handle button 2 click event."""
        print("Button 2 clicked")

if __name__ == "__main__":
    root = Tk()
    app = KasirApp(root)
    root.mainloop()
