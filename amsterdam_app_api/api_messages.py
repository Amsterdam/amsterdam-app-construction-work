""" Common messages returned by API. Just import 'Messages' and get all messages at once (hence the class)
"""


class Messages:
    def __init__(self):
        self.invalid_query = 'Invalid query parameter(s). See /api/v1/apidocs for more information'
        self.no_record_found = 'No record found'
        self.access_denied = 'ACCESS DENIED'
        self.do_not_match = 'Passwords do not match'
        self.invalid_username_or_password = 'Invalid username or password'
        self.distance_params = 'Use either street + num or lat/lon'
        self.unsupported_image_format = 'Unsupported image format'
