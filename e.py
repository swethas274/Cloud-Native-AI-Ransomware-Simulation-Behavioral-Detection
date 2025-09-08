#!/usr/bin/env python3
# fernet_encryptor.py

import os
from cryptography.fernet import Fernet

def fernet_encrypt_data(plaintext):
    """
    Encrypts data using Fernet symmetric encryption.
    :param plaintext: Bytes data to encrypt
    :return: Tuple of (ciphertext, key) where both are bytes
    """
    # Generate a new key for this encryption
    key = Fernet.generate_key()
    
    # Create Fernet cipher instance with the key
    cipher = Fernet(key)
    
    # Encrypt the plaintext
    ciphertext = cipher.encrypt(plaintext)
    
    return ciphertext, key

def fernet_decrypt_data(ciphertext, key):
    """
    Decrypts data using Fernet symmetric encryption.
    :param ciphertext: Encrypted bytes data
    :param key: The Fernet key used for encryption
    :return: Decrypted plaintext bytes
    """
    cipher = Fernet(key)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

# Example usage and test
if __name__ == "__main__":
    # Test the encryption/decryption
    test_data = b"Hello, this is a secret message for testing Fernet encryption!"
    
    print("Original data:", test_data)
    
    # Encrypt
    encrypted, key = fernet_encrypt_data(test_data)
    print("Encrypted:", encrypted)
    print("Encryption key:", key.hex())
    
    # Decrypt (to verify it works)
    decrypted = fernet_decrypt_data(encrypted, key)
    print("Decrypted:", decrypted)
    print("Decryption successful:", decrypted == test_data)
    
    # Test with file encryption (like your original script)
    print("\n" + "="*50)
    print("File encryption demo:")
    
    # Create a test file
    test_filename = "test_file.txt"
    with open(test_filename, "w") as f:
        f.write("This is some test content for file encryption.")
    
    # Encrypt the file
    with open(test_filename, "rb") as f:
        file_content = f.read()
    
    encrypted_content, file_key = fernet_encrypt_data(file_content)
    
    # Save encrypted file
    encrypted_filename = "test_file.encrypted"
    with open(encrypted_filename, "wb") as f:
        f.write(encrypted_content)
    
    # Save the key
    key_filename = "test_key.key"
    with open(key_filename, "wb") as f:
        f.write(file_key)
    
    print(f"File '{test_filename}' encrypted to '{encrypted_filename}'")
    print(f"Key saved to '{key_filename}'")
    
    # Clean up test files
    os.remove(test_filename)
    os.remove(encrypted_filename)
    os.remove(key_filename)
