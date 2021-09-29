from django.test import TestCase
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher


class TestHashing(TestCase):
    def test_encryption_ok(self):
        test_string = 'test string'
        aes = AESCipher(test_string, 'secret')
        encrypted = aes.encrypt()
        aes.data = encrypted
        cleartext = aes.decrypt()
        self.assertEqual(test_string, cleartext)

    def test_encrypt_fail(self):
        aes = AESCipher(b'', 'secret')
        result = aes.encrypt()
        self.assertEqual(result, None)

    def test_decrypt_fail(self):
        aes = AESCipher(b'', 'secret')
        result = aes.decrypt()
        self.assertEqual(result, None)
