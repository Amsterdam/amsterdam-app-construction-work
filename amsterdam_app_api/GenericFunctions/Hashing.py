import hashlib


class Hashing:
    @staticmethod
    def make_md5_hash(string):
        return hashlib.md5(string.encode()).hexdigest()

    @staticmethod
    def make_sha1_hash(string):
        return hashlib.sha1(string.encode()).hexdigest()
