#!/usr/bin/env python3
# data_generator.py
import os
import argparse
from pathlib import Path

# Import from your specific files
from dynamic_e import morphing_encrypt  # Instead of morphing_encryptor
from e import fernet_encrypt_data       # Instead of fernet_encryptor

def generate_dataset(samples=100, plaintext_size=1024, output_dir="../data"):
    """
    Generates the dataset of encrypted files.
    """
    # Create the output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"[+] Generating {samples} samples in '{output_dir}'...")

    for i in range(samples):
        # 1. Generate random plaintext bytes
        plaintext = os.urandom(plaintext_size)
        
        # 2. Save the plaintext
        plain_file = output_path / f"sample_{i:05d}_plain.bin"
        with open(plain_file, 'wb') as f:
            f.write(plaintext)
        
        # 3. Encrypt with MORPHING Algorithm and save
        seed = i  # Use sample number as seed for reproducibility
        morph_ciphertext = morphing_encrypt(plaintext, seed=seed)
        
        morph_file = output_path / f"sample_{i:05d}_morph_seed_{seed}.bin"
        with open(morph_file, 'wb') as f:
            f.write(morph_ciphertext)
        
        # 4. Encrypt with FERNET Algorithm and save
        fernet_ciphertext, fernet_key = fernet_encrypt_data(plaintext)
        
        fernet_file = output_path / f"sample_{i:05d}_fernet.bin"
        with open(fernet_file, 'wb') as f:
            f.write(fernet_ciphertext)
        
        # Optional: Save the Fernet key (useful for decryption tests later)
        key_file = output_path / f"sample_{i:05d}_fernet_key.key"
        with open(key_file, 'wb') as f:
            f.write(fernet_key)
        
        # Print progress every 100 samples
        if (i + 1) % 100 == 0:
            print(f"    Generated {i + 1}/{samples} samples...")
    
    print(f"[+] Dataset generation complete! Files saved to {output_dir}")

if __name__ == "__main__":
    # Configure from command line
    parser = argparse.ArgumentParser(description='Generate encryption dataset for AI training.')
    parser.add_argument('--samples', type=int, default=1000, help='Number of samples to generate')
    parser.add_argument('--size', type=int, default=512, help='Size of each sample in bytes')
    parser.add_argument('--output', type=str, default="../data", help='Output directory')
    
    args = parser.parse_args()
    
    # Start the generation process
    generate_dataset(samples=args.samples, plaintext_size=args.size, output_dir=args.output)
