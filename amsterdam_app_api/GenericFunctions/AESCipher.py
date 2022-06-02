from Crypto import Random
from amsterdam_app_api.GenericFunctions.Logger import Logger
from Crypto.Cipher import AES
from hashlib import md5
from pybase64 import b64encode, b64decode


class AESCipher:
    def __init__(self, data, secret):
        self.logger = Logger()
        self.data = data
        self.secret = secret.encode()
        self.block_size = 16
        self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def bytes_to_key(self, data, salt, output=48):
        assert len(salt) == 8, len(salt)
        data += salt
        key = md5(data).digest()
        final_key = key
        while len(final_key) < output:
            key = md5(key + data).digest()
            final_key += key
        return final_key[:output]

    def encrypt(self):
        try:
            salt = Random.new().read(8)
            key_iv = self.bytes_to_key(self.secret, salt, 32+16)
            key = key_iv[:32]
            iv = key_iv[32:]
            aes = AES.new(key, AES.MODE_CBC, iv)
            return b64encode(b"Salted__" + salt + aes.encrypt(self.pad(self.data).encode())).decode()
        except Exception as error:
            self.logger.error(error)
            return None

    def decrypt(self):
        try:
            encrypted = b64decode(self.data)
            assert encrypted[0:8] == b"Salted__"
            salt = encrypted[8:16]
            key_iv = self.bytes_to_key(self.secret, salt, 32+16)
            key = key_iv[:32]
            iv = key_iv[32:]
            aes = AES.new(key, AES.MODE_CBC, iv)
            return self.unpad(aes.decrypt(encrypted[16:])).decode()
        except Exception as error:
            self.logger.error(error)
            return None

