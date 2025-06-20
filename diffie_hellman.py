#!/usr/bin/env python3

import secrets
import sympy

default_bit_size = 128
private_key_bit_size = default_bit_size // 2

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

def generate_private_key(bits=private_key_bit_size):
    """Generate a private key smaller than the prime modulus"""
    return secrets.randbits(bits) 