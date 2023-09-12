""" unit_tests """
from django.test import TestCase

from construction_work.generic_functions.aes_cipher import AESCipher


class TestHashing(TestCase):
    """Unittest aes cyphers"""

    def test_encrypt_decrypt_success(self):
        """test encrypt ok"""
        test_string = "test string"
        aes = AESCipher(test_string, "secret")
        encrypted = aes.encrypt()
        aes.data = encrypted
        cleartext = aes.decrypt()
        self.assertEqual(test_string, cleartext)

    def test_encrypt_fail(self):
        """test encrypt fail"""
        aes = AESCipher(b"", "secret")
        result = aes.encrypt()
        self.assertEqual(result, None)

    def test_decrypt_fail(self):
        """test decrypt fail"""
        aes = AESCipher(b"", "secret")
        result = aes.decrypt()
        self.assertEqual(result, None)
