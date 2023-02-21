""" UNITTESTS """

from django.test import TestCase
from amsterdam_app_api.GenericFunctions.Hashing import Hashing


class TestHashing(TestCase):
    """ Unittest for convenient library hashing """
    def test_make_md5_hash(self):
        """ Test create md5 hash """
        data = 'mock'
        hashing = Hashing()
        result = hashing.make_md5_hash(data)

        self.assertEqual(result, '17404a596cbd0d1e6c7d23fcd845ab82')

    def test_make_sha1_hash(self):
        """ Test create sha1 hash """
        data = 'mock'
        hashing = Hashing()
        result = hashing.make_sha1_hash(data)

        self.assertEqual(len(result), 40)
