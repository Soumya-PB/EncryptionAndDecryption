from caesar_cipher import CaesarCipher


def test_caesar_encrypt_decrypt_roundtrip():
	shift = 3
	cipher = CaesarCipher(shift)

	message = "Hello, World!"

	encrypted = cipher.encrypt(message)
	decrypted = cipher.decrypt(encrypted)

	assert decrypted == message