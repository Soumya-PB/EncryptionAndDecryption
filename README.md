# 🔐 Encryption and Decryption Tool

A Python-based desktop application developed using **Tkinter** that allows users to securely encrypt and decrypt both **text** and **files** using **AES Encryption** and the **Caesar Cipher**. The application provides a simple graphical interface suitable for learning cryptography concepts and demonstrating secure data protection techniques.

---

## 📌 Features

- 🔒 AES Text Encryption
- 🔓 AES Text Decryption
- 🔐 Caesar Cipher Encryption
- 🔓 Caesar Cipher Decryption
- 📂 File Encryption
- 📂 File Decryption
- 🔑 Password-Based Encryption
- 🖥️ User-Friendly Tkinter GUI
- 📋 Clear Input & Output
- ⚠️ Error Handling and Input Validation

---

## 🛠️ Technologies Used

- Python 3.x
- Tkinter
- Cryptography (Fernet)
- hashlib
- base64
- os
- pathlib

---

## 📂 Project Structure

```
EncryptionAndDecryption/
│
├── aes_cipher.py
├── caesar_cipher.py
├── file_handler.py
├── key_manager.py
├── main.py
├── requirements.txt
├── README.md
│
├── encrypted_files/
├── decrypted_files/
├── keys/
│
├── sample.txt
├── test_aes.py
├── test_file_handler.py
└── test_key_manager.py
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/Soumya-PB/EncryptionAndDecryption.git
```

Navigate into the project folder:

```bash
cd EncryptionAndDecryption
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python main.py
```

---

# 🔐 AES Encryption

AES (Advanced Encryption Standard) is a symmetric encryption algorithm where the same password is used for both encryption and decryption.

### Features

- Password-Based Encryption
- Secure Key Generation
- Fernet Encryption
- Base64 Encoded Output

Example

Input

```
Hello World
```

Encrypted

```
gAAAAAB...
```

---

# 🔐 Caesar Cipher

The Caesar Cipher is a substitution cipher where each letter is shifted by a fixed number.

Example

Shift = 3

Input

```
HELLO
```

Encrypted

```
KHOOR
```

Decrypted

```
HELLO
```

---

# 📂 File Encryption

The application supports encryption and decryption of files.

Supported file types include:

- txt
- pdf
- docx
- csv
- png
- jpg
- jpeg

Encrypted files are stored in

```
encrypted_files/
```

Decrypted files are stored in

```
decrypted_files/
```
## Screenshots
<img width="1105" height="906" alt="Screenshot 2026-07-10 222200" src="https://github.com/user-attachments/assets/ee74000a-2fc3-4072-bd48-117b92645184" />

<img width="1091" height="900" alt="Screenshot 2026-07-10 224558" src="https://github.com/user-attachments/assets/38c26e0f-38bd-4b80-bcd7-cb1f87a10470" />

<img width="763" height="617" alt="Screenshot 2026-07-10 230027" src="https://github.com/user-attachments/assets/b2f6caee-a1df-48c5-96a4-80e2675be81b" />

<img width="1233" height="997" alt="image" src="https://github.com/user-attachments/assets/c11ba231-259d-4b5d-bc53-853fbd7e06fb" />

---

## GUI Overview

The application provides:

- AES / Caesar Selection
- Password Input
- Shift Value
- Text Encryption
- Text Decryption
- File Selection
- Encrypt File
- Decrypt File
- Output Display
- Status Bar

---

## Project Workflow

```
User Input
      │
      ▼
Select Algorithm
      │
      ├──────── AES
      │           │
      │           ▼
      │     Encrypt/Decrypt
      │
      └──────── Caesar
                  │
                  ▼
           Encrypt/Decrypt
                  │
                  ▼
            Display Result
```


### File Encryption

> Add another screenshot here

```
screenshots/file_encryption.png
```

---

## Future Enhancements

- RSA Encryption
- DES Encryption
- Triple DES
- Blowfish
- Drag and Drop File Support
- Dark/Light Theme
- Export Encrypted Text
- Clipboard Support
- Password Strength Meter
- File Progress Bar

---

## Learning Outcomes

This project demonstrates:

- Python GUI Development
- Cryptography Fundamentals
- AES Encryption
- Caesar Cipher
- File Handling
- Object-Oriented Programming
- Exception Handling
- Secure Password-Based Encryption


## Repository

https://github.com/Soumya-PB/EncryptionAndDecryption
