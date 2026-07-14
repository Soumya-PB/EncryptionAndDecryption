from pathlib import Path
from file_handler import FileHandler

handler = FileHandler()

# Password for both encryption and decryption
password = "soumya@123"

# Get the project directory (where this script is located)
project_dir = Path(__file__).parent

# Full path to sample.txtfrom file_handler import FileHandler
fh = FileHandler()
out = fh.encrypt_file(r"C:\path\to\your\file.txt", "soumya@123")
print("Saved to:", out)
sample_file = project_dir / "sample.txt"

# Check if the file exists
if not sample_file.exists():
    print(f"ERROR: File not found:\n{sample_file}")
    exit()

print("Encrypting File...")

encrypted_path = handler.encrypt_file(str(sample_file), password)

if isinstance(encrypted_path, str) and encrypted_path.startswith("ERROR"):
    print(encrypted_path)
else:
    print("Encrypted File Saved At:")
    print(encrypted_path)

    print("\nDecrypting File...")

    decrypted_path = handler.decrypt_file(encrypted_path, password)

    if isinstance(decrypted_path, str) and decrypted_path.startswith("ERROR"):
        print(decrypted_path)
    else:
        print("Decrypted File Saved At:")
        print(decrypted_path)