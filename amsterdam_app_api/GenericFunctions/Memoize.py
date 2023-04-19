""" Python memoize decorator

    Copyright:

    https://github.com/masikh/Memoize is licensed under the GNU General Public License v3.0

    Permissions of this strong copyleft license are conditioned on making available complete source code of licensed
    works and modifications, which include larger works using a licensed work, under the same license. Copyright and
    license notices must be preserved. Contributors provide an express grant of patent rights.

    Introduction:

    The class provided in this repository can be imported into your project and used as a decorator
    for any method. It has the ability to cache the output of a function provided that the
    method takes at least one argument (read: argument, not keyword argument!). The _first_
    argument is used as a key for storing the cache into a dictionary.

    Example usage:

    Let's assume we're dealing with a django-view file where a user can look up students
    by year of registration and see how many students there are present in the building.

    from Memoize import Memoize

    memoize = Memoize(ttl=300, max_items=100)

    @api_view(['GET'])
    @memoize
    def students(year, age=None):
        query = {'year': year}
        if age:
            query['age'] = age
        _students = list(Student.objects.objects.filter(**query).all())
        ...
        return Response(result)

    @api_view(['GET'])
    @memoize(ttl=5)
    def in_classroom(building):
        query = {'building': building}
        _students = list(InClassRoom.objects.objects.filter(**query).all())
        ...
        return Response(result)

    In above example you can use the memoize decorator with a predefined `ttl` in seconds or override
    the `ttl` for a specific use case.

    Behaviour:

    - When the `ttl` has expired for a cached item, the cache is invalid and will be cleared on next call.
    - When the amount of items exceeds the `max_items`, items with will be purged by ttl until `max_items` are
      present in the cache
    - `ttl` can be overriden for a specific use case by setting the `ttl` in the decorator as a `kwarg`
    - `max_items` and `ttl` are set to a chosen value on class initialization, when omitted they default to
      `ttl:` 300 seconds and `max_items:` 128 items.

    Dependencies:

    Memoize depends on the python build-ins `time` and `functools`
"""
import time
import functools


class Memoize:
    """ Example usage:

        memoize = Memoize(ttl=300, max_items=100)

        @memoize
        def students(year, age=None):
            query = {'year': year}
            if age:
                query['age'] = age
            _students = list(Student.objects.objects.filter(**query).all())
            ...
            return result

        @memoize(ttl=5)
        def signed_in(building):
            query = {'building': building}
            _students = list(SignedIn.objects.objects.filter(**query).all())
            ...
            return result
    """
    def __init__(self, ttl=300, max_items=128):
        self.memoize_cache = {}
        self.ttl = ttl
        self.max_items = max_items

    def add_cache(self, key, value, ttl):
        """ Store cache item """
        self.memoize_cache[key] = (time.time() + ttl, value)

    def clean_cache(self):
        """ Clear expired cached items """
        now = time.time()
        self.memoize_cache = {key: value for key, value in self.memoize_cache.items() if now <= value[0]}

        # Remove all items more than self.max_items by cache-age
        sorted_cache = sorted(self.memoize_cache.items(), key=lambda x: x[1][0], reverse=False)
        for key, value in sorted_cache:
            if len(self.memoize_cache) - self.max_items <= 0:
                break
            del self.memoize_cache[key]

    def __call__(self, func=None, ttl=None):
        if func is None:
            return functools.partial(self.__call__, ttl=ttl)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Set ttl for this cache item
            _ttl = self.ttl if ttl is None else ttl

            # Check if key in cache
            if args[0] in self.memoize_cache:
                # if key is not expired, return result
                if time.time() - self.memoize_cache[args[0]][0] <= _ttl:
                    result = self.memoize_cache[args[0]][1]
                    self.clean_cache()
                    return result

                # Remove expired key
                del self.memoize_cache[args[0]]

            # Cache miss, execute the function and fill the cache
            result = func(*args, **kwargs)
            self.add_cache(args[0], result, _ttl)
            self.clean_cache()
            return result
        return wrapper
