from key_manager import KeyManager

manager = KeyManager()

print("Checking for existing key...")

if manager.key_exists():
    print("Key already exists!")

    key = manager.load_key()

else:
    print("No key found.")

    key = manager.generate_key()

    manager.save_key(key)

    print("New key generated and saved!")

print("\nEncryption Key:")
print(key.decode())