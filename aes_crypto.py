#!/usr/bin/env python3

import secrets
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def derive_aes_key(shared_key):
    """Derive a 256-bit AES key from the shared key using HKDF.
    HKDF (HMAC-based Extract-and-Expand Key Derivation Function) is a key derivation function
    that takes a shared secret and expands it into a larger, cryptographically secure key,
    such as a 256-bit AES key.
    """
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

class SessionKey:
    """A class to manage a session key derived from a shared secret.
    This allows efficient encryption/decryption by deriving the AES key once
    and reusing it for multiple messages.
    """

    def __init__(self, shared_key):
        """Initialize the session with a shared key and derive the AES key once."""
        self.aes_key = derive_aes_key(shared_key)

    def encrypt_message(self, message):
        """Encrypt the message using the pre-derived AES key"""
        # Convert message to bytes
        message_bytes = message.encode()

        # Generate a random IV (Initialization Vector)
        iv = secrets.token_bytes(16)

        # Create an encryptor
        cipher = Cipher(
            algorithms.AES(self.aes_key),
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

    def decrypt_message(self, encrypted_message):
        """Decrypt the message using the pre-derived AES key"""
        # Decode base64 and split IV from encrypted data
        encrypted_data = base64.b64decode(encrypted_message)
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]

        # Create a decryptor
        cipher = Cipher(
            algorithms.AES(self.aes_key),
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

# Legacy functions for backward compatibility
def encrypt_message(message, shared_key):
    """Legacy function that creates a temporary session for single message encryption.
    For multiple messages, use SessionKey class for better performance.
    """
    session = SessionKey(shared_key)
    return session.encrypt_message(message)

def decrypt_message(encrypted_message, shared_key):
    """Legacy function that creates a temporary session for single message decryption.
    For multiple messages, use SessionKey class for better performance.
    """
    session = SessionKey(shared_key)
    return session.decrypt_message(encrypted_message)