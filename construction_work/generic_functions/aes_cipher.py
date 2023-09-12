""" AESCipher: Encrypts and de-crypts data
"""
from hashlib import md5

from Crypto import Random
from Crypto.Cipher import AES
from pybase64 import b64decode, b64encode


class AESException(Exception):
    """Exception class for AES"""
    pass


class AESCipher:
    """AESCipher class implementation"""

    def __init__(self, data, secret):
        self.data = data
        self.secret = secret.encode()
        self.blk_size = 16
        self.pad = lambda s: s + (self.blk_size - len(s) % self.blk_size) * chr(
            self.blk_size - len(s) % self.blk_size
        )
        self.unpad = lambda s: s[: -ord(s[len(s) - 1 :])]

    def bytes_to_key(self, data, salt, output=48):
        """Convert byte to key"""
        assert len(salt) == 8, len(salt)
        data += salt
        key = md5(data).digest()
        final_key = key
        while len(final_key) < output:
            key = md5(key + data).digest()
            final_key += key
        return final_key[:output]

    def encrypt(self):
        """Encrypt string"""
        try:
            salt = Random.new().read(8)
            key_iv = self.bytes_to_key(self.secret, salt, 32 + self.blk_size)
            key = key_iv[:32]
            iv = key_iv[32:]
            aes = AES.new(key, AES.MODE_CBC, iv)
            return b64encode(
                b"Salted__" + salt + aes.encrypt(self.pad(self.data).encode())
            ).decode()
        except Exception as e:
            raise AESException(e)

    def decrypt(self):
        """Decrypt string"""
        try:
            # Convert base64-encoded ciphertext into binary representation
            encrypted = b64decode(self.data)
            # Cipher should have been prepared with a random salt value before encryption
            assert encrypted[0:8] == b"Salted__"
            salt = encrypted[8:16]
            # Derive encryption key and initialization vector
            # Key = 32 bytes, IV = 16 bytes
            key_iv = self.bytes_to_key(self.secret, salt, 32 + self.blk_size)
            key = key_iv[:32]
            iv = key_iv[32:]
            # Initializes AES cipher object
            aes = AES.new(key, AES.MODE_CBC, iv)
            # Decrypt encrypted data and remove padding
            decrypted_cipher = aes.decrypt(encrypted[16:])
            unpadded_cipher = self.unpad(decrypted_cipher)
            return unpadded_cipher.decode()
        except Exception as e:
            raise AESException(e)
