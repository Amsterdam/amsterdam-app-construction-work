""" Common messages returned by API. Just import 'Messages' and get all messages at once (hence the class)
"""


class Messages:
    def __init__(self):
        self.invalid_query = 'Invalid query parameter(s). See /api/v1/apidocs for more information'
        self.no_record_found = 'No record found'