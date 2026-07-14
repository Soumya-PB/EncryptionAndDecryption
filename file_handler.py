"""
file_handler.py
Handles reading, saving, encrypting, and decrypting text files.
"""

import os
import time
from aes_cipher import AESCipher
from caesar_cipher import CaesarCipher


class FileHandler:

    ENCRYPTED_FOLDER = "encrypted_files"
    DECRYPTED_FOLDER = "decrypted_files"
    BINARY_EXTS = ('.pdf', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.docx', '.xlsx', '.pptx', '.doc', '.xls', '.ppt', '.zip')

    def __init__(self):
        os.makedirs(self.ENCRYPTED_FOLDER, exist_ok=True)
        os.makedirs(self.DECRYPTED_FOLDER, exist_ok=True)

    def read_text_file(self, filepath):
        """
        Read a text file.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            return f"ERROR: {e}"

    def save_text_file(self, filepath, data):
        """
        Save text to a file.
        """
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(data)
            return True
        except Exception as e:
            return f"ERROR: {e}"

    def encrypt_file(self, filepath, auth_value, algorithm="AES", save=True, overwrite=False):
        """
        Encrypt a text file using AES or Caesar.
        """
        if algorithm == "AES":
            return self._encrypt_aes(filepath, auth_value, save=save, overwrite=overwrite)
        elif algorithm == "Caesar":
            return self._encrypt_caesar(filepath, auth_value, save=save, overwrite=overwrite)
        else:
            return "ERROR: Unsupported algorithm"

    def _encrypt_aes(self, filepath, password, save=True, overwrite=False):
        try:
            cipher = AESCipher(password)
            # Handle binary files (PDF, images, office docs)
            if filepath.lower().endswith(self.BINARY_EXTS):
                # For binary files we require saving to disk or overwrite
                if not save and not overwrite:
                    return "ERROR: Binary file encryption requires saving to disk (enable Save or Overwrite)."
                with open(filepath, 'rb') as f:
                    data = f.read()
                encrypted_bytes = cipher.encrypt_bytes(data)
                if overwrite:
                    output_path = filepath
                    mode = 'wb'
                else:
                    filename = os.path.basename(filepath)
                    output_path = os.path.join(self.ENCRYPTED_FOLDER, filename + ".enc")
                    mode = 'wb'
                try:
                    with open(output_path, mode) as file:
                        file.write(encrypted_bytes)
                    return output_path
                except PermissionError:
                    # Attempt fallback to encrypted folder with a unique name
                    try:
                        filename = os.path.basename(filepath)
                        alt_name = f"{int(time.time())}_{filename}.enc"
                        alt_path = os.path.join(self.ENCRYPTED_FOLDER, alt_name)
                        with open(alt_path, 'wb') as file:
                            file.write(encrypted_bytes)
                        return alt_path
                    except Exception as e:
                        return f"ERROR: Permission denied writing to {output_path}: {e}"

            # Text file path
            text = self.read_text_file(filepath)
            if text.startswith("ERROR"):
                return text
            encrypted = cipher.encrypt_text(text)
            if not save:
                return encrypted
            if overwrite:
                output_path = filepath
            else:
                filename = os.path.basename(filepath)
                output_path = os.path.join(self.ENCRYPTED_FOLDER, filename + ".enc")
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(encrypted)
            return output_path
        except Exception as e:
            return f"ERROR: {e}"

    def _encrypt_caesar(self, filepath, shift, save=True, overwrite=False):
        try:
            cipher = CaesarCipher(int(shift))
            text = self.read_text_file(filepath)
            if text.startswith("ERROR"):
                return text
            encrypted = cipher.encrypt(text)
            if not save:
                return encrypted
            if overwrite:
                output_path = filepath
            else:
                filename = os.path.basename(filepath)
                output_path = os.path.join(self.ENCRYPTED_FOLDER, filename + ".caesar")
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(encrypted)
            return output_path
        except Exception as e:
            return f"ERROR: {e}"

    def decrypt_file(self, filepath, auth_value, algorithm="AES", save=True, overwrite=False):
        """
        Decrypt an encrypted text file using AES or Caesar.
        """
        if algorithm == "AES":
            return self._decrypt_aes(filepath, auth_value, save=save, overwrite=overwrite)
        elif algorithm == "Caesar":
            return self._decrypt_caesar(filepath, auth_value, save=save, overwrite=overwrite)
        else:
            return "ERROR: Unsupported algorithm"

    def _decrypt_aes(self, filepath, password, save=True, overwrite=False):
        try:
            cipher = AESCipher(password)
            # Binary file path: determine if target is binary by extension or original name
            name = os.path.basename(filepath)
            is_binary = False
            if name.lower().endswith('.enc'):
                base = name[:-4]
                if base.lower().endswith(self.BINARY_EXTS):
                    is_binary = True
            elif name.lower().endswith(self.BINARY_EXTS):
                is_binary = True

            if is_binary:
                # Try reading as bytes
                try:
                    with open(filepath, 'rb') as f:
                        encrypted_bytes = f.read()
                    decrypted = cipher.decrypt_bytes(encrypted_bytes)
                    if isinstance(decrypted, str) and decrypted.startswith("ERROR"):
                        return decrypted
                    # decrypted is bytes
                    if not save:
                        return decrypted
                    if overwrite:
                        output_path = filepath
                    else:
                        filename = os.path.basename(filepath)
                        # remove .enc if present
                        if filename.endswith('.enc'):
                            filename = filename[:-4]
                        output_path = os.path.join(self.DECRYPTED_FOLDER, filename)
                    try:
                        with open(output_path, 'wb') as file:
                            file.write(decrypted)
                        return output_path
                    except PermissionError:
                        try:
                            filename = os.path.basename(filepath)
                            alt_name = f"{int(time.time())}_{filename}"
                            alt_path = os.path.join(self.DECRYPTED_FOLDER, alt_name)
                            with open(alt_path, 'wb') as file:
                                file.write(decrypted)
                            return alt_path
                        except Exception as e:
                            return f"ERROR: Permission denied writing to {output_path}: {e}"
                except Exception:
                    # Fall back to text path below
                    pass

            # Text file path
            with open(filepath, "r", encoding="utf-8") as file:
                encrypted = file.read()
            decrypted = cipher.decrypt_text(encrypted)
            if decrypted.startswith("ERROR"):
                return decrypted
            if not save:
                return decrypted
            if overwrite:
                output_path = filepath
            else:
                filename = os.path.basename(filepath)
                if filename.endswith(".enc"):
                    filename = filename[:-4]
                output_path = os.path.join(self.DECRYPTED_FOLDER, filename)
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(decrypted)
            return output_path
        except Exception as e:
            return f"ERROR: {e}"

    def _decrypt_caesar(self, filepath, shift, save=True, overwrite=False):
        try:
            cipher = CaesarCipher(int(shift))
            text = self.read_text_file(filepath)
            if text.startswith("ERROR"):
                return text
            decrypted = cipher.decrypt(text)
            if not save:
                return decrypted
            if overwrite:
                output_path = filepath
            else:
                filename = os.path.basename(filepath)
                if filename.endswith(".caesar"):
                    filename = filename[:-7]
                output_path = os.path.join(self.DECRYPTED_FOLDER, filename)
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(decrypted)
            return output_path
        except Exception as e:
            return f"ERROR: {e}"
