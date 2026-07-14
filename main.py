import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox, filedialog

from file_handler import FileHandler

from aes_cipher import AESCipher
from caesar_cipher import CaesarCipher

# Optional drag-and-drop support via tkinterdnd2
try:
    from tkinter import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except Exception:
    DND_AVAILABLE = False



class EncryptionApp:

    def select_file(self):
        file = filedialog.askopenfilename(
            filetypes=[
                ("Text files", "*.txt"),
                ("Encrypted files", "*.enc *.caesar"),
                ("All files", "*.*")
            ]
        )

        if file:
            self.selected_file = file
            self.file_label.config(text=file)
            self.status.config(text="File selected")
            self.update_file_status()

    def handle_drop(self, event):
        data = event.data
        try:
            files = self.root.tk.splitlist(data)
        except Exception:
            files = [data]

        if not files:
            return

        file = files[0].strip("{}")
        self.selected_file = file
        self.file_label.config(text=file)
        self.status.config(text="File selected via drag-and-drop")
        self.update_file_status()

    def update_file_status(self):
        if not self.selected_file:
            return
        name = os.path.basename(self.selected_file)
        if name.endswith(".enc"):
            status = "Selected file looks AES encrypted (.enc)"
        elif name.endswith(".caesar"):
            status = "Selected file looks Caesar encrypted (.caesar)"
        else:
            status = "Selected file appears unencrypted."
        if hasattr(self, "file_status"):
            self.file_status.config(text=status)

    def __init__(self, root):

        self.root = root

        self.root.title("Secure Cryptography Tool")

        self.root.geometry("900x820")
        self.root.minsize(900, 820)

        self.root.configure(bg="#2C3E50")

        self.root.resizable(True, True)

        self.file_handler = FileHandler()
        self.selected_file = None
        self.last_saved_path = None

        self.build_gui()

    # ============================
    # Encrypt Function
    # ============================

    def encrypt_text(self):
        text = self.input_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning("Warning", "Please enter text")
            return

        # AES path
        if self.algorithm.get() == "AES":
            password = self.password_entry.get()
            if len(password) < 6:
                messagebox.showerror(
                    "Error",
                    "Password must contain at least 6 characters."
                )
                return

            cipher = AESCipher(password)
            encrypted = cipher.encrypt_text(text)

        # Caesar path
        else:
            try:
                shift = int(self.shift_entry.get())
                if shift < 1 or shift > 25:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Shift must be between 1 and 25.")
                return

            cipher = CaesarCipher(shift)
            encrypted = cipher.encrypt(text)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, encrypted)
        self.status.config(text="Encryption Successful")
            


    # ============================
    # Decrypt Function
    # ============================

    def decrypt_text(self):

        input_text = self.input_text.get(
            "1.0",
            tk.END
        ).strip()
        output_text = self.output_text.get(
            "1.0",
            tk.END
        ).strip()

        if output_text:
            text = output_text
        elif input_text:
            text = input_text
        else:
            messagebox.showwarning(
                "Warning",
                "Enter encrypted text"
            )
            return

        def do_decrypt(value):
            if self.algorithm.get() == "AES":
                password = self.password_entry.get()
                if len(password) < 6:
                    messagebox.showerror(
                        "Error",
                        "Password must contain at least 6 characters."
                    )
                    return None

                cipher = AESCipher(password)
                return cipher.decrypt_text(value)
            else:
                try:
                    shift = int(self.shift_entry.get())
                    if shift < 1 or shift > 25:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Error", "Shift must be between 1 and 25.")
                    return None

                cipher = CaesarCipher(shift)
                return cipher.decrypt(value)

        decrypted = do_decrypt(text)
        if decrypted is None:
            return

        if isinstance(decrypted, str) and decrypted.startswith("ERROR:"):
            error_message = decrypted.replace("ERROR:", "", 1).strip()
            if not error_message:
                error_message = "Invalid Password or Corrupted Data"
            messagebox.showerror(
                "Error",
                error_message
            )
            self.status.config(text="Decryption Failed")
            return

        self.output_text.delete(
            "1.0",
            tk.END
        )
        self.output_text.insert(
            tk.END,
            decrypted
        )
        self.status.config(
            text="Decryption Successful"
        )


    def encrypt_file(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a file to encrypt.")
            return

        algorithm = self.algorithm.get()
        save = bool(self.save_files_var.get())
        overwrite = bool(self.overwrite_file_var.get())

        if algorithm == "AES":
            password = self.password_entry.get()
            if len(password) < 6:
                messagebox.showerror("Error", "Password must contain at least 6 characters.")
                return
            if overwrite:
                if not messagebox.askyesno("Confirm overwrite", "Overwrite the selected file in place? This will replace the original file. Continue?"):
                    return
            result = self.file_handler.encrypt_file(
                self.selected_file,
                password,
                algorithm="AES",
                save=save,
                overwrite=overwrite
            )
        else:
            try:
                shift = int(self.shift_entry.get())
                if shift < 1 or shift > 25:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Shift must be between 1 and 25.")
                return
            if overwrite:
                if not messagebox.askyesno("Confirm overwrite", "Overwrite the selected file in place? This will replace the original file. Continue?"):
                    return
            result = self.file_handler.encrypt_file(
                self.selected_file,
                shift,
                algorithm="Caesar",
                save=save,
                overwrite=overwrite
            )

        if isinstance(result, str) and result.startswith("ERROR"):
            messagebox.showerror("Error", result)
            self.status.config(text="Encryption Failed")
        else:
            # If result is a path to a saved file, read and display its contents
            if isinstance(result, str) and os.path.exists(result):
                try:
                    # Save the path for preview; don't auto-open
                    self.last_saved_path = result
                    # Try to read the saved file as text; if it fails or returns an ERROR string, treat as binary
                    file_contents = self.file_handler.read_text_file(result)

                    if isinstance(file_contents, str) and file_contents and not file_contents.startswith("ERROR"):
                        self.output_text.delete("1.0", tk.END)
                        self.output_text.insert(tk.END, file_contents)
                        messagebox.showinfo("Success", f"Encrypted file saved to: {result}")
                        self.status.config(text="File Encryption Successful (viewing file)")
                    else:
                        messagebox.showinfo("Success", f"Encrypted file saved to: {result}\nUse Preview to open binary files.")
                        self.status.config(text="File Encryption Successful")
                except Exception:
                    messagebox.showinfo("Success", f"Encrypted file saved to: {result}")
                    self.status.config(text="File Encryption Successful")
            else:
                # In-memory result (not saved to disk)
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, result)
                self.status.config(text="File Encrypted (in-memory)")
                # clear last saved path when result is in-memory
                self.last_saved_path = None


    def decrypt_file(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select a file to decrypt.")
            return

        algorithm = self.algorithm.get()
        save = bool(self.save_files_var.get())
        overwrite = bool(self.overwrite_file_var.get())

        if algorithm == "AES":
            password = self.password_entry.get()
            if len(password) < 6:
                messagebox.showerror("Error", "Password must contain at least 6 characters.")
                return
            if overwrite:
                if not messagebox.askyesno("Confirm overwrite", "Overwrite the selected file in place? This will replace the original file. Continue?"):
                    return
            result = self.file_handler.decrypt_file(
                self.selected_file,
                password,
                algorithm="AES",
                save=save,
                overwrite=overwrite
            )
        else:
            try:
                shift = int(self.shift_entry.get())
                if shift < 1 or shift > 25:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Shift must be between 1 and 25.")
                return
            if overwrite:
                if not messagebox.askyesno("Confirm overwrite", "Overwrite the selected file in place? This will replace the original file. Continue?"):
                    return
            result = self.file_handler.decrypt_file(
                self.selected_file,
                shift,
                algorithm="Caesar",
                save=save,
                overwrite=overwrite
            )

        if isinstance(result, str) and result.startswith("ERROR"):
            messagebox.showerror("Error", result)
            self.status.config(text="Decryption Failed")
        else:
            # If result is a path to a saved file, read and display its contents
            if isinstance(result, str) and os.path.exists(result):
                try:
                    # Save the path for preview; don't auto-open
                    self.last_saved_path = result
                    # Try to read the saved file as text; if it fails or returns an ERROR string, treat as binary
                    file_contents = self.file_handler.read_text_file(result)

                    if isinstance(file_contents, str) and file_contents and not file_contents.startswith("ERROR"):
                        self.output_text.delete("1.0", tk.END)
                        self.output_text.insert(tk.END, file_contents)
                        messagebox.showinfo("Success", f"Decrypted file saved to: {result}")
                        self.status.config(text="File Decryption Successful (viewing file)")
                    else:
                        messagebox.showinfo("Success", f"Decrypted file saved to: {result}\nUse Preview to open binary files.")
                        self.status.config(text="File Decryption Successful")
                except Exception:
                    messagebox.showinfo("Success", f"Decrypted file saved to: {result}")
                    self.status.config(text="File Decryption Successful")
            else:
                # In-memory result (not saved to disk)
                self.output_text.delete("1.0", tk.END)
                # If result is bytes (binary), convert to a hex preview to avoid errors
                if isinstance(result, (bytes, bytearray)):
                    try:
                        preview = result.decode('utf-8', errors='replace')
                    except Exception:
                        preview = str(result)
                    self.output_text.insert(tk.END, preview)
                else:
                    self.output_text.insert(tk.END, result)
                self.status.config(text="File Decrypted (in-memory)")
                # clear last saved path when result is in-memory
                self.last_saved_path = None


    # ============================
    # Clear Function
    # ============================

    def clear_text(self):
        self.password_entry.delete(0, tk.END)
        self.shift_entry.delete(0, tk.END)
        self.shift_entry.insert(0, "3")
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)


    # ============================
    # GUI Design
    # ============================

    def build_gui(self):

        container = tk.Frame(self.root, bg="#2C3E50")
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg="#2C3E50", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scroll_frame = tk.Frame(self.canvas, bg="#2C3E50")
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.scroll_frame.bind("<Configure>", on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        title = tk.Label(
            self.scroll_frame,
            text="Secure Cryptography Tool",
            font=("Arial",22,"bold"),
            bg="#2C3E50",
            fg="white"
        )

        title.pack(pady=15)



        # Algorithm Selection

        algorithm_frame = tk.LabelFrame(
            self.scroll_frame,
            text="Algorithm",
            bg="#34495E",
            fg="white",
            font=("Arial",11,"bold")
        )

        algorithm_frame.pack(
            fill="x",
            padx=20
        )


        self.algorithm = tk.StringVar(
            value="AES"
        )


        tk.Radiobutton(
            algorithm_frame,
            text="AES",
            variable=self.algorithm,
            value="AES",
            bg="#34495E",
            fg="white",
            selectcolor="#34495E"
        ).pack(
            side="left",
            padx=20
        )


        tk.Radiobutton(
            algorithm_frame,
            text="Caesar Cipher",
            variable=self.algorithm,
            value="Caesar",
            bg="#34495E",
            fg="white",
            selectcolor="#34495E"
        ).pack(
            side="left",
            padx=20
        )



        # Password

        tk.Label(
            self.scroll_frame,
            text="Password",
            bg="#2C3E50",
            fg="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=5
        )


        self.password_entry = tk.Entry(
            self.scroll_frame,
            width=40,
            show="*"
        )

        self.password_entry.pack(
            padx=20
        )

        self.save_files_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            self.scroll_frame,
            text="Save encrypted/decrypted files to folder",
            variable=self.save_files_var,
            bg="#2C3E50",
            fg="white",
            selectcolor="#2C3E50",
            activebackground="#2C3E50",
            activeforeground="white",
            highlightthickness=0,
            bd=0
        ).pack(
            anchor="w",
            padx=20,
            pady=(10,0)
        )

        self.overwrite_file_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            self.scroll_frame,
            text="Overwrite selected file in place",
            variable=self.overwrite_file_var,
            bg="#2C3E50",
            fg="white",
            selectcolor="#2C3E50",
            activebackground="#2C3E50",
            activeforeground="white",
            highlightthickness=0,
            bd=0
        ).pack(
            anchor="w",
            padx=20,
            pady=(5,10)
        )

        # Shift

        tk.Label(
            self.scroll_frame,
            text="Caesar Shift (1-25)",
            bg="#2C3E50",
            fg="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=5
        )


        self.shift_entry = tk.Entry(
            self.scroll_frame,
            width=10
        )

        self.shift_entry.insert(
            0,
            "4"
        )

        self.shift_entry.pack(
            padx=20
        )


        # File Encryption UI
        file_frame = tk.LabelFrame(
            self.scroll_frame,
            text="File Encryption",
            bg="#34495E",
            fg="white",
            font=("Arial", 11, "bold")
        )

        file_frame.pack(fill="x", padx=20, pady=15)

        tk.Button(
            file_frame,
            text="Select File",
            command=self.select_file,
            width=15
        ).grid(row=0, column=0, padx=10, pady=10)

        tk.Button(
            file_frame,
            text="Encrypt File",
            command=self.encrypt_file,
            bg="#27AE60",
            fg="white",
            width=15
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            file_frame,
            text="Decrypt File",
            command=self.decrypt_file,
            bg="#2980B9",
            fg="white",
            width=15
        ).grid(row=0, column=2, padx=10)

        tk.Button(
            file_frame,
            text="Preview",
            command=self.preview_file,
            width=12
        ).grid(row=0, column=3, padx=10)

        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            bg="#34495E",
            fg="white"
        )

        self.file_label.grid(row=1, column=0, columnspan=3, pady=(0, 5))

        self.file_info = tk.Label(
            file_frame,
            text="Select a file first, then click Encrypt File or Decrypt File.",
            bg="#34495E",
            fg="white",
            font=("Arial", 9)
        )

        self.file_info.grid(row=2, column=0, columnspan=3, pady=(0, 10))

        self.file_status = tk.Label(
            file_frame,
            text="Selected file appears unencrypted.",
            bg="#34495E",
            fg="white",
            font=("Arial", 9, "italic")
        )
        self.file_status.grid(row=3, column=0, columnspan=3, pady=(0, 10))

        if DND_AVAILABLE:
            try:
                self.file_label.drop_target_register(DND_FILES)
                self.file_label.dnd_bind('<<Drop>>', self.handle_drop)
            except Exception:
                pass


        text_frame = tk.LabelFrame(
            self.scroll_frame,
            text="Text Encryption",
            bg="#34495E",
            fg="white",
            font=("Arial",11,"bold")
        )

        text_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        tk.Label(
            text_frame,
            text="Input Text",
            bg="#34495E",
            fg="white",
            font=("Arial",12,"bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=10
        )

        self.input_text = ScrolledText(
            text_frame,
            width=100,
            height=8
        )

        self.input_text.pack(
            padx=20,
            pady=(0,10)
        )


        # Buttons

        button_frame = tk.Frame(
            text_frame,
            bg="#2C3E50"
        )

        button_frame.pack(
            pady=(0,10)
        )

        tk.Button(
            button_frame,
            text="Encrypt",
            width=15,
            bg="#27AE60",
            fg="white",
            command=self.encrypt_text
        ).grid(
            row=0,
            column=0,
            padx=6
        )


        tk.Button(
            button_frame,
            text="Decrypt",
            width=15,
            bg="#2980B9",
            fg="white",
            command=self.decrypt_text
        ).grid(
            row=0,
            column=1,
            padx=10
        )


        tk.Button(
            button_frame,
            text="Clear",
            width=15,
            bg="#E67E22",
            fg="white",
            command=self.clear_text
        ).grid(
            row=0,
            column=2,
            padx=10
        )




        tk.Label(
            text_frame,
            text="Enter text above and click Encrypt Text or Decrypt Text. Result appears in the Output box below.",
            bg="#34495E",
            fg="#ECF0F1",
            font=("Arial",10,"italic")
        ).pack(
            anchor="w",
            padx=20,
            pady=(0,10)
        )

        output_frame = tk.LabelFrame(
            text_frame,
            text="Output",
            bg="#34495E",
            fg="white",
            font=("Arial",12,"bold"),
            bd=2,
            relief="groove"
        )

        output_frame.pack(
            fill="x",
            padx=20,
            pady=(0,15)
        )

        self.output_text = ScrolledText(
            output_frame,
            width=100,
            height=8,
            bg="#ffffff",
            fg="#000000",
            wrap=tk.WORD,
            bd=1,
            relief="sunken"
        )

        self.output_text.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # Status

        self.status = tk.Label(
            self.root,
            text="Ready",
            anchor="w",
            bg="#1B2631",
            fg="white"
        )

        self.status.pack(
            side="bottom",
            fill="x"
        )

    def preview_file(self):
        # Open the last saved path if available, otherwise the selected file
        path = None
        if hasattr(self, 'last_saved_path') and self.last_saved_path:
            path = self.last_saved_path
        elif self.selected_file:
            path = self.selected_file

        if not path:
            messagebox.showwarning("Warning", "No file to preview.")
            return

        if not os.path.exists(path):
            messagebox.showwarning("Warning", f"File does not exist: {path}")
            return

        try:
            os.startfile(path)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open file: {e}")



def main():

    # Use TkinterDnD root if available for drag-and-drop support
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()

    app = EncryptionApp(root)

    root.mainloop()



if __name__ == "__main__":
    main()