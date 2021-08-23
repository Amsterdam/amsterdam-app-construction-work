class SetFilter:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get(self):
        filter_dict = dict()
        for kwarg in self.kwargs:
            if self.kwargs[kwarg] is not None:
                filter_dict[kwarg] = self.kwargs[kwarg]
        return filter_dict
