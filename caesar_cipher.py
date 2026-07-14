"""
caesar_cipher.py
Caesar Cipher Encryption & Decryption Module
"""


class CaesarCipher:

    def __init__(self, shift: int):
        """
        Initialize the cipher with a shift value.
        Shift must be between 1 and 25.
        """
        if not (1 <= shift <= 25):
            raise ValueError("Shift value must be between 1 and 25.")

        self.shift = shift

    def encrypt(self, text: str) -> str:
        """
        Encrypt text using Caesar Cipher.
        """
        result = ""

        for char in text:

            # Uppercase letters
            if char.isupper():
                result += chr((ord(char) - 65 + self.shift) % 26 + 65)

            # Lowercase letters
            elif char.islower():
                result += chr((ord(char) - 97 + self.shift) % 26 + 97)

            # Numbers, spaces and symbols remain unchanged
            else:
                result += char

        return result

    def decrypt(self, text: str) -> str:
        """
        Decrypt Caesar Cipher text.
        """
        result = ""

        for char in text:

            if char.isupper():
                result += chr((ord(char) - 65 - self.shift) % 26 + 65)

            elif char.islower():
                result += chr((ord(char) - 97 - self.shift) % 26 + 97)

            else:
                result += char

        return result