from time import time

"""

Inspired by:
http://code.activestate.com/recipes/325905-memoize-decorator-with-timeout/
"""


class Cache(object):
    """Function cache object. Do not call this directly.
    """
    def __init__(self, func, timeout, purgedepth=None):
        """
        func: function that is subject of memoization
        timeout: age (in seconds) that a cached result remains valid
        purgedepth: how much effort will be put into keeping the cache
                    scrubbed. By default, attempt to automatically
                    contain length
        """
        self.name = "%s:%s"%(func.__module__, func.__name__)
        self.timeout = timeout
        self.purgedepth = purgedepth
        self.hwm = 0

        self.purge()

    def _key(self, args, kwargs):
        kw = kwargs.items()
        return (args, tuple(sorted(kw)))

    def lookup(self, args, kwargs):
        """
        Find a cached result for the function call, else raise KeyError
        """
        key = self._key(args, kwargs)
        if key not in self.cache:
            self.misses += 1
            raise KeyError

        if self.expiry[key]>time():
            self.hits += 1
            return self.cache[key]

        self.timeouts += 1
        raise KeyError

    def add(self, args, kwargs, result):
        """
        Add a new entry to the cache for this function, and remove the
        oldest expired entries.

        The downside to this approach is that we will always take
        slightly longer to return a result in the case that we encounter
        a cache miss.  The upside is that we shouldn't need to worry
        about running a separate garbage collection mechanism.

        This only works if we are smart about how we inspect the list
        of potential candidates to purge. To do this, we keep a FIFO of
        the memoized items and so only need to inspect the beginning of
        the list.
        """
        now = time()
        key = self._key(args, kwargs)
        self.expiry[key] = self.timeout + now
        self.cache[key] = result
        self.refs.append(key)
        self.hwm = max(self.hwm, len(self.cache))

        try:
            purgedepth = self.purgedepth
            if not purgedepth:
                purgedepth = min(3, len(self.cache)*0.05)

            while purgedepth:
                purgedepth = purgedepth-1
                key = self.refs[0]
                if self.expiry[key]<now:
                    del self.expiry[key]
                    del self.cache[key]
                    self.refs.pop(0)
                else:
                    break
        except KeyError:
            pass

    def reset(self):
        self.hits = 0
        self.misses = 0
        self.timeouts = 0

    def purge(self):
        self.cache = {}
        self.expiry = {}
        self.refs = []

        self.reset()
        
    def stats(self):
        return {
                "cache": self.name,
                "hits": self.hits,
                "misses": self.misses,
                "timeouts": self.timeouts,
                "length": len(self.cache),
                "hwm": self.hwm,
                }


class mwt(object):
    """Memoize With Timeout
    
    """

    _caches = {}

    def __init__(self, timeout=2, purgedepth=None):
        """Memoize decorator
        
        Args:
            timeout (int): interval in seconds to keep cache entries alive
            purgedepth (int): number of entries to attempt to purge each add cycle

        Unless a value is specified, memoize will attempt to automatically
        determine how many entries to purge.
        """
        self.timeout = timeout
        self.purgedepth = purgedepth

    @staticmethod
    def reset():
        """Reset counters on all of the funtion caches
        """
        return [cache.reset() for func, cache in mwt._caches.items()]

    @staticmethod
    def purge():
        """Purge all function caches and reset counters
        """
        return [cache.purge() for func, cache in mwt._caches.items()]

    @staticmethod
    def stats():
        """Reap statistics from individual function caches

        This method will return a list of dicts, one from each function cache.

            "cache": The name of the function being memoized
            "hits": The numer of times a cache hit occurred
            "misses": The numer of times a cache miss occurred
            "timeouts": The numer of times a cache hit found a timed-out value
            "length": The current number of entries in the cache
            "hwm": The highest number of entries in the cache
        """
        return [cache.stats() for func, cache in mwt._caches.items()]

    def __call__(self, f):
        try:
            cache = mwt._caches[f]
        except:
            cache = mwt._caches[f] = Cache(f, self.timeout, self.purgedepth)

        def func(*args, **kwargs):
            try:
                return cache.lookup(args, kwargs)
            except KeyError:
                result = f(*args, **kwargs)
                cache.add(args, kwargs, result)

                return result

        func.__name__ = f.__name__

        return func
