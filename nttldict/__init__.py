import datetime
import shelve
from contextlib import contextmanager


class NaiveTTLDict:
    """
    Naive dict-like class with expiration
    """

    def __init__(self, default_ttl=None):
        self._backend = dict()
        self.default_ttl = default_ttl

    @property
    @contextmanager
    def backend(self):
        yield self._backend

    def __iter__(self):
        with self.backend as cache:
            self._clear_expired(cache)
            # We have to evaluate full __iter__ before closing the shelve!
            return iter(list(cache.__iter__()))

    def __len__(self):
        with self.backend as cache:
            self._clear_expired(cache)
            return len(cache)

    def __contains__(self, key):
        with self.backend as cache:
            self._clear_expired(cache)
            return cache.__contains__(key)

    def __getitem__(self, key):
        with self.backend as cache:
            self._clear_expired(cache, key)
            if key in cache:
                return cache[key]["data"]

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __delitem__(self, key):
        with self.backend as cache:
            return cache.__delitem__(key)

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default

    def set(self, key, value, ttl=None):
        tmp = {"data": value, "expires_on": None}
        expiration = ttl or self.default_ttl
        if expiration:
            tmp["expires_on"] = datetime.datetime.now() + datetime.timedelta(
                seconds=expiration
            )

        with self.backend as cache:
            cache[key] = tmp

    def pop(self, key, default=None):
        value = self.get(key, default)
        try:
            self.__delitem__(key)
        except KeyError:
            pass
        return value

    def keys(self):
        with self.backend as cache:
            self._clear_expired(cache)
            return list(cache.keys())

    def items(self):
        with self.backend as cache:
            self._clear_expired(cache)
            return list(map(lambda x: (x[0], x[1]["data"]), cache.items()))

    def values(self):
        with self.backend as cache:
            self._clear_expired(cache)
            return list(map(lambda x: x["data"], cache.values()))

    def clear(self):
        with self.backend as cache:
            return cache.clear()

    def update(self, other):
        raise NotImplementedError

    def _clear_expired(self, cache, key=None):
        def is_expired(data):
            ttl = data["expires_on"]
            return ttl and ttl < datetime.datetime.now()

        keys_to_expire = []

        loop = [key] if key and key in cache else cache
        for key in loop:
            if is_expired(cache[key]):
                keys_to_expire.append(key)

        for key in keys_to_expire:
            del cache[key]


class NaiveTTLDictDisk(NaiveTTLDict):
    """
    Naive dict-like class with expiration, persisted on disk
    """

    def __init__(self, filename, default_ttl=None):
        super().__init__(default_ttl)
        self._backend = filename

    @property
    def backend(self):
        return shelve.open(filename=self._backend, writeback=True)
