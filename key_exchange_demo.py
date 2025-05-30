#!/usr/bin/env python3

import secrets
import sympy
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

default_bit_size = 128

alices = "Alice's"
bobs = "Bob's"
pub_key_str = "public key"
pri_key_str = "private key"
shared_key_str = "shared key"

def execute_key_exchange():
    print("\nThis script demonstrates a key exchange between two parties, Alice and Bob. It is based on the Diffie-Hellman key exchange algorithm, which is a public key cryptography algorithm. The purpose is to establish a shared secret key between the two parties without exchanging any secrets.")
    print("\nThe two main calculations are:")
    print("  1. A function to generate large prime numbers")
    print("  2. ((a^b) mod c) for asymmetric encryption")
    print(f"\nNote: To speed things up we use smaller key sizes ({default_bit_size} bits) instead of full 2048-bit primes.")
    input("\nPress Enter to continue to Step 1...")

    print("\nStep 1\nBoth parties agree on public parameters.")
    print("The prime modulus and generator are public parameters, i.e. they are not secrets.")
    print("The prime modulus is a large prime number.")
    print("The generator can be a small integer (often 2 or 5), and its size does not impact security as much as the size and properties of the prime modulus.")
    prime_modulus = calc_prime()
    print(f"Calculate prime modulus: {prime_modulus}")
    generator = 5
    print(f"Select generator: {generator}")
    input("\nPress Enter to continue to Step 2...")

    print("\nStep 2\nEach party generates a private key - a large prime - using the same function as used for the prime modulus in the previous step.")
    print("The private keys are secrets!")
    alice_pri_key = calc_prime()
    print(f"{alices} {pri_key_str}: {alice_pri_key}")
    bob_pri_key = calc_prime()
    print(f"{bobs} {pri_key_str}: {bob_pri_key}")
    input("\nPress Enter to continue to Step 3...")

    print("\nStep 3\nEach party computes their public key - (generator^priv_key mod prime_modulus).")
    alice_pub_key = calc_key(generator, alice_pri_key, prime_modulus)
    print(f"{alices} {pub_key_str}: {alice_pub_key}")
    bob_pub_key = calc_key(generator, bob_pri_key, prime_modulus)
    print(f"{bobs} {pub_key_str}: {bob_pub_key}")
    input("\nPress Enter to continue to Step 4...")

    print("\nStep 4\nAfter each party has exchanged their public keys, they compute the shared secret key - (other_party_pub_key^priv_key mod prime_modulus)")
    alice_shared_key = calc_key(bob_pub_key, alice_pri_key, prime_modulus)
    print(f"{alices} {shared_key_str}: {alice_shared_key}")
    bob_shared_key = calc_key(alice_pub_key, bob_pri_key, prime_modulus)
    print(f"{bobs} {shared_key_str}: {bob_shared_key}")

    print("\nCheck if the shared keys are the same")
    if alice_shared_key == bob_shared_key:
        print(f"Shared keys match: {alice_shared_key}")
    else:
        print(f"Shared keys do not match: {alice_shared_key} != {bob_shared_key}")
    input("\nPress Enter to continue to Step 5...")

    print("\nStep 5\nAlice uses the shared secret key to encrypt and send a message to Bob")
    message = "Hello, world!"
    print(f"{alices} message: {message}")
    encrypted_message = encrypt_message(message, alice_shared_key)
    print(f"Encrypted message: {encrypted_message}")
    input("\nPress Enter to continue to Step 6...")
    
    print(f"\nStep 6\nBob receives the message, and decrypts it using his shared secret key")
    decrypted_message = decrypt_message(encrypted_message, bob_shared_key)
    print(f"Bob reads the decrypted message: {decrypted_message}")
    input("\nPress Enter to continue to finish...")

    print("\nNote that during the whole process, no secrets were exchanged.\n")

def calc_key(generator, key, prime):
    """(generator^key) % prime"""
    return pow(generator, key, prime)

def calc_prime(bits=default_bit_size):
    """Calculate a large prime number suitable for cryptographic operations"""
    while True:
        # Generate a random odd number of appropriate size
        # The OR operation ensures the last bit is set to 1 to guarantee the number is odd
        candidate = secrets.randbits(bits) | 1
        # primality test
        if sympy.isprime(candidate):
            return candidate

def generate_private_key(bits=default_bit_size):
    """Generate a smaller private key (256 bits is sufficient for security)"""
    return secrets.randbits(bits)

def derive_aes_key(shared_key):
    """Derive a 256-bit AES key from the shared key using HKDF"""
    # Convert shared key to bytes
    shared_key_bytes = str(shared_key).encode()
    
    # Use HKDF to derive a key
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits
        salt=None,
        info=b'key_exchange_demo',
        backend=default_backend()
    )
    return hkdf.derive(shared_key_bytes)

def encrypt_message(message, shared_key):
    """Encrypt the message using AES-256 in CBC mode"""
    # Convert message to bytes
    message_bytes = message.encode()
    
    # Derive AES key from shared key
    key = derive_aes_key(shared_key)
    
    # Generate a random IV (Initialization Vector)
    iv = secrets.token_bytes(16)
    
    # Create an encryptor
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    
    # Pad the message
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message_bytes) + padder.finalize()
    
    # Encrypt the padded message
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Combine IV and encrypted data and encode as base64
    return base64.b64encode(iv + encrypted_data).decode()

def decrypt_message(encrypted_message, shared_key):
    """Decrypt the message using AES-256 in CBC mode"""
    # Decode base64 and split IV from encrypted data
    encrypted_data = base64.b64decode(encrypted_message)
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    
    # Derive AES key from shared key
    key = derive_aes_key(shared_key)
    
    # Create a decryptor
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Unpad the data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    # Convert back to string
    return data.decode()

execute_key_exchange()
