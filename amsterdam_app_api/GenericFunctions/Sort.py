from amsterdam_app_api.GenericFunctions.Logger import Logger


class Sort:
    """ Sort list of dictionaries by key in ascending or descending order
    """
    def __init__(self):
        self.logger = Logger()

    def list_of_dicts(self, items, key=None, sort_order='asc'):
        try:
            if key is not None:
                reverse = sort_order == 'desc'

                if reverse is True:
                    result = sorted(items, key=lambda x: (x[key] is not None, x[key]), reverse=True)
                else:
                    result = sorted(items, key=lambda x: (x[key] is None, x[key]))
                return result
        except Exception as error:
            self.logger.error('Caught error in Sort.list_of_dicts: {error}'.format(error=error))
        return items
