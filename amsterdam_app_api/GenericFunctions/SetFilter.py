""" SetFilter is used as a single way to set DB filtering based on kwargs. It saves a lot of duplicate and
    cluttering code from the views_*_.py where we'd like to return DB results based on set query parameters.

    If the value of a keyword is None, it will be omitted from the filter.

    e.g.:

    {'a': None, 'b': 1} will become {'b': 1}
"""


class SetFilter:
    """ Filter class """
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get(self):
        """ set filter from self.kwargs """
        filter_dict = {}
        for key, value in self.kwargs.items():
            if value is not None:
                filter_dict[key] = value
        return filter_dict
