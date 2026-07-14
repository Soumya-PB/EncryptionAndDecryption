"""
key_manager.py
Generate, Save and Load Encryption Keys
"""

import os
from cryptography.fernet import Fernet


class KeyManager:

    KEY_FOLDER = "keys"
    KEY_FILE = os.path.join(KEY_FOLDER, "secret.key")

    def __init__(self):
        os.makedirs(self.KEY_FOLDER, exist_ok=True)

    def generate_key(self):
        """
        Generate a new Fernet key.
        """
        return Fernet.generate_key()

    def save_key(self, key):
        """
        Save the key to secret.key.
        """
        try:
            with open(self.KEY_FILE, "wb") as file:
                file.write(key)

            return True

        except Exception as e:
            return f"ERROR: {e}"

    def load_key(self):
        """
        Load the key from secret.key.
        """
        try:
            with open(self.KEY_FILE, "rb") as file:
                return file.read()

        except FileNotFoundError:
            return None

        except Exception as e:
            return f"ERROR: {e}"

    def key_exists(self):
        """
        Check whether the key file exists.
        """
        return os.path.exists(self.KEY_FILE)