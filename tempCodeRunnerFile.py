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
