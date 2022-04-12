def firebase_admin_messaging_send_multicast(args):
    class response:
        def __init__(self, success):
            self.success = success

    class Response:
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
    def __init__(self, *args, **kwargs):
        self.content = '{"results": [{"centroid": [0, -90]}]}'
