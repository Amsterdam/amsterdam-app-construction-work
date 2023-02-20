""" Unittest mock functions (prevent calling actual 3th parties ) """


def firebase_admin_messaging_send_multicast(args):
    """ Mock sending multicast message to devices via firebase """
    class response:
        """ Mock response from firebase """
        def __init__(self, success):
            self.success = success

    class Response:
        """ Mock (outer) response class """
        def __init__(self, args):
            self.args = args
            self.failure_count = 1
            self.responses = []
            for i in range(0, len(args.tokens)):
                if i == 0:
                    self.responses.append(response(False))
                else:
                    self.responses.append(response(True))

    return Response(args)


class address_to_coordinates:
    """ Mock address to coordinates response from 3rd party API """
    def __init__(self, *args, **kwargs):
        self.content = '{"results": [{"centroid": [0, -90]}]}'
