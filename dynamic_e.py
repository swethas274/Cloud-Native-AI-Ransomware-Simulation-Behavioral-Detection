#!/usr/bin/env python3
# morphing_encryptor.py
import numpy as np

# Define a list of encryption operations. Each operates on a single byte (0-255).
def op_xor(byte, key_byte):
    return byte ^ key_byte

def op_add(byte, key_byte):
    return (byte + key_byte) % 256

def op_sub(byte, key_byte):
    return (byte - key_byte) % 256

def op_mul(byte, key_byte):
    return (byte * key_byte) % 256

def op_bitshift_left(byte, key_byte, rng):
    # Use the provided seeded RNG to get a reproducible random number
    shift_amount = rng.integers(1, 7) # Let's choose a sensible range, e.g., 1-6
    return (byte << shift_amount) % 256

def op_bitshift_right(byte, key_byte, rng):
    # Use the provided seeded RNG to get a reproducible random number
    shift_amount = rng.integers(1, 7)
    return byte >> shift_amount

# List of all available operations
# NOTE: We now need to know which functions need the extra 'rng' argument.
# We'll handle this in the main loop.
OPERATIONS_NEED_RNG = [op_bitshift_left, op_bitshift_right]
OPERATIONS_NORMAL = [op_xor, op_add, op_sub, op_mul]

def morphing_encrypt(plaintext, seed=12345):
    """
    Encrypts data using a morphing algorithm determined by a seed.
    :param plaintext: Bytes to encrypt
    :param seed: Integer to determine the encryption sequence
    :return: Ciphertext bytes
    """
    # Initialize a pseudo-random number generator with our seed
    rng = np.random.default_rng(seed)

    # Generate a stream of key bytes
    key_stream = rng.bytes(len(plaintext) * 5)
    key_index = 0

    # Generate the sequence of operations to apply (3-5 ops per byte)
    num_operations = rng.integers(3, 6)
    # Choose from all operations
    all_ops = OPERATIONS_NORMAL + OPERATIONS_NEED_RNG
    op_sequence = rng.choice(all_ops, size=num_operations, replace=True)

    # Convert plaintext to a mutable bytearray
    ciphertext = bytearray(plaintext)

    # Apply each operation in the sequence to every byte in the data
    for op_func in op_sequence:
        for i in range(len(ciphertext)):
            key_byte = key_stream[key_index % len(key_stream)]
            key_index += 1

            # Check if this function needs the RNG object passed to it
            if op_func in OPERATIONS_NEED_RNG:
                new_byte = op_func(ciphertext[i], key_byte, rng)
            else:
                new_byte = op_func(ciphertext[i], key_byte)

            ciphertext[i] = new_byte % 256 # Ensure it stays a byte

    return bytes(ciphertext)


# Simple test to verify it works
if __name__ == "__main__":
    test_data = b"Hello World! This is a test message."
    print("Original:", test_data)

    encrypted_data = morphing_encrypt(test_data, seed=42)
    print("Encrypted:", encrypted_data)
    print("Hex:", encrypted_data.hex())

    # Test with a different seed
    encrypted_data2 = morphing_encrypt(test_data, seed=999)
    print("Encrypted (seed=999):", encrypted_data2.hex())
    print("Are they different?", encrypted_data != encrypted_data2)

    # CRITICAL TEST: Reproducibility
    print("\nTesting Reproducibility with seed=42:")
    encrypted_again = morphing_encrypt(test_data, seed=42)
    print("Same result both times?", encrypted_data == encrypted_again)
    # This MUST print "True" for the project to work.
