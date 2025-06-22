#!/usr/bin/env python3

import os
from diffie_hellman import calc_prime, calc_key, generate_private_key
from aes_crypto import encrypt_message, decrypt_message, SessionKey

# Constants for display
alices = "Alice's"
bobs = "Bob's"
pub_key_str = "public key"
pri_key_str = "private key"
shared_key_str = "shared key"
default_bit_size = 128

def clear_screen():
    """Clear the terminal screen"""
    # Clear screen for Windows
    if os.name == 'nt':
        os.system('cls')
    # Clear screen for Unix/Linux/macOS
    else:
        os.system('clear')

def print_step(step_number):
    """Print a step header with the given number"""
    print(f"\n\n-------\nStep {step_number}\n-------")

def wait_for_enter():
    """Print the continue prompt and wait for user input"""
    input("\nPress Enter to continue...")

def run_demo():
    clear_screen()
    print("\nThis script demonstrates a key exchange between two parties, Alice and Bob. It is based on the classical Diffie-Hellman key exchange algorithm, which is a public key cryptography algorithm. The purpose is to establish a shared secret key between the two parties without exchanging any secrets.")
    print("\nThe two main calculations are:")
    print("  1. A function to generate large prime numbers")
    print("  2. ((a^b) mod c) for asymmetric encryption")
    print(f"\nNote: To speed things up we use smaller key sizes ({default_bit_size} bits) instead of full 2048-bit primes.")
    wait_for_enter()

    print_step(1)
    print("Both parties agree on public parameters.")
    print("The prime modulus and generator are public parameters, i.e. they are not secrets.")
    print("The prime modulus is a large prime number.")
    print("The generator can be a small integer (often 2 or 5), and its size does not impact security as much as the size and properties of the prime modulus.")
    prime_modulus = calc_prime()
    print(f"\nCalculate prime modulus: {prime_modulus}")
    generator = 5
    print(f"Select generator: {generator}")
    wait_for_enter()

    print_step(2)
    print("Each party generates a private key - a random number smaller than the prime modulus.")
    print("The private keys are secrets!")
    alice_pri_key = generate_private_key()
    print(f"\n{alices} {pri_key_str}: {alice_pri_key}")
    bob_pri_key = generate_private_key()
    print(f"{bobs} {pri_key_str}:   {bob_pri_key}")
    wait_for_enter()

    print_step(3)
    print("Each party computes their public key:\n(generator^priv_key mod prime_modulus).")
    alice_pub_key = calc_key(generator, alice_pri_key, prime_modulus)
    print(f"\n{alices} {pub_key_str}: {alice_pub_key}")
    bob_pub_key = calc_key(generator, bob_pri_key, prime_modulus)
    print(f"{bobs} {pub_key_str}:   {bob_pub_key}")
    wait_for_enter()

    print_step(4)
    print("After each party has exchanged their public keys, they compute the shared secret key:\n(other_party_pub_key^priv_key mod prime_modulus)")
    alice_shared_key = calc_key(bob_pub_key, alice_pri_key, prime_modulus)
    print(f"\n{alices} {shared_key_str}: {alice_shared_key}")
    bob_shared_key = calc_key(alice_pub_key, bob_pri_key, prime_modulus)
    print(f"{bobs} {shared_key_str}:   {bob_shared_key}")
    wait_for_enter()

    print_step(5)
    print("Each party derives their AES-256 key from the shared secret using HKDF (HMAC-based Extract-and-Expand Key Derivation Function).\nThis key will be used for symmetric encryption.")
    alice_session = SessionKey(alice_shared_key)
    bob_session = SessionKey(bob_shared_key)
    print(f"\n{alices} derived AES key (hex): {alice_session.aes_key.hex()}")
    print(f"{bobs} derived AES key (hex):   {bob_session.aes_key.hex()}")
    wait_for_enter()

    print_step(6)
    print("Alice uses the shared secret key to encrypt and send a message to Bob")
    message = "Hello, world!"
    print(f"\n{alices} message:   {message}")
    encrypted_message = alice_session.encrypt_message(message)
    print(f"Encrypted message: {encrypted_message}")
    wait_for_enter()
    
    print_step(7)
    print(f"Bob receives the message, and decrypts it using his shared secret key")
    decrypted_message = bob_session.decrypt_message(encrypted_message)
    print(f"\nBob reads the decrypted message: {decrypted_message}")
    input("\nPress Enter to finish...\n\n")

    print("-"*62)
    print("Note that during the whole process, no secrets were exchanged!")
    print("-"*62)

if __name__ == "__main__":
    run_demo() 