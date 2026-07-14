"""
aes_cipher.py
AES-256 Encryption & Decryption Module
"""

import base64
import hashlib

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken


class AESCipher:
    """
    AES Encryption using Fernet (AES-128 in CBC mode with HMAC authentication).
    A password is converted into a secure key using SHA-256.
    """

    def __init__(self, password: str):
        self.password = password
        self.key = self.generate_key(password)
        self.cipher = Fernet(self.key)

    @staticmethod
    def generate_key(password: str) -> bytes:
        """
        Convert password into a 32-byte Fernet key.
        """
        sha = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(sha)

    def encrypt_text(self, text: str) -> str:
        """
        Encrypt plain text.
        """
        encrypted = self.cipher.encrypt(text.encode())
        return encrypted.decode()

    def encrypt_bytes(self, data: bytes) -> bytes:
        """
        Encrypt raw bytes (for binary files such as PDF).
        Returns encrypted bytes on success.
        """
        return self.cipher.encrypt(data)

    def decrypt_text(self, encrypted_text: str) -> str:
        """
        Decrypt encrypted text.
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_text.encode())
            return decrypted.decode()

        except InvalidToken:
            return "ERROR: Invalid Password or Corrupted Data"

        except Exception as e:
            return f"ERROR: {e}"

    def decrypt_bytes(self, encrypted_bytes: bytes):
        """
        Decrypt encrypted bytes (for binary files).
        Returns bytes on success or an error string starting with "ERROR:" on failure.
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted
        except InvalidToken:
            return "ERROR: Invalid Password or Corrupted Data"
        except Exception as e:
            return f"ERROR: {e}"