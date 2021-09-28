from amsterdam_app_api.GenericFunctions.Logger import Logger
from Crypto.Cipher import AES
from Crypto.Random import new as Random
from hashlib import sha256
from pybase64 import b64encode, b64decode


class AESCipher:
    def __init__(self, data, secret):
        self.logger = Logger()
        self.block_size = 16
        self.data = data
        self.key = sha256(secret.encode('utf-8')).digest()[:32]
        self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self):
        try:
            plain_text = self.pad(self.data)
            iv = Random().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CFB, iv)

            return b64encode(iv + cipher.encrypt(plain_text.encode())).decode()
        except Exception as error:
            self.logger.error(error)
            return None

    def decrypt(self):
        try:
            cipher_text = b64decode(self.data.encode())
            iv = cipher_text[:self.block_size]
            cipher = AES.new(self.key, AES.MODE_CFB, iv)
            return self.unpad(cipher.decrypt(cipher_text[self.block_size:])).decode()
        except Exception as error:
            self.logger.error(error)
            return None
