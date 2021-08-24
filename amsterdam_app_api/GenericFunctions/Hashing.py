import hashlib


class Hashing:
    """ Return a hash based on input string (Used for eg. setting identifiers, create secret key for backend etc..)
    """
    @staticmethod
    def make_md5_hash(string):
        """ Static HASH. eg. multiple iterations of the same input yields same output
        """
        return hashlib.md5(string.encode()).hexdigest()

    @staticmethod
    def make_sha1_hash(string):
        """ Non-Static HASH. eg. multiple iterations of the same input yields different output
        """
        return hashlib.sha1(string.encode()).hexdigest()
