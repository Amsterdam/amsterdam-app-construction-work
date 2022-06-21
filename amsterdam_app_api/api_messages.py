""" Common messages returned by API. Just import 'Messages' and get all messages at once (hence the class)
"""


class Messages:
    def __init__(self):
        self.access_denied = 'ACCESS DENIED'
        self.distance_params = 'Use either street + num or lat/lon'
        self.do_not_match = 'Passwords do not match'
        self.invalid_headers = 'Invalid header(s). See /api/v1/apidocs for more information'
        self.invalid_query = 'Invalid query parameter(s). See /api/v1/apidocs for more information'
        self.invalid_username_or_password = 'Invalid username or password'
        self.no_record_found = 'No record found'
        self.no_such_database_model = 'No such database model'
        self.no_such_field_in_model = 'No such field in database model'
        self.unsupported_image_format = 'Unsupported image format'
