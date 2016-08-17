# urllib3/_collections.py
##

##

##

##


from collections import deque

from threading import RLock

__all__ = ['RecentlyUsedContainer']


class AccessEntry(object):
    __slots__ = ('key', 'is_valid')

    def __init__(self, key, is_valid=True):
        self.key = key
        self.is_valid = is_valid


class RecentlyUsedContainer(dict):
    ''''''


    ##

    ##

    ##

    CLEANUP_FACTOR = 10

    def __init__(self, maxsize=10):
        self._maxsize = maxsize

        self._container = {}

        ##

        self.access_log = deque()
        self.access_log_lock = RLock()

        ##

        ##

        ##

        self.access_lookup = {}

        ##

        self.access_log_limit = maxsize * self.CLEANUP_FACTOR

    def _invalidate_entry(self, key):
        ''''''

        old_entry = self.access_lookup.get(key)
        if old_entry:
            old_entry.is_valid = False

        return old_entry

    def _push_entry(self, key):
        ''''''

        self._invalidate_entry(key)

        new_entry = AccessEntry(key)
        self.access_lookup[key] = new_entry

        self.access_log_lock.acquire()
        self.access_log.appendleft(new_entry)
        self.access_log_lock.release()

    def _prune_entries(self, num):
        ''''''

        while num > 0:
            self.access_log_lock.acquire()
            p = self.access_log.pop()
            self.access_log_lock.release()

            if not p.is_valid:
                continue ##


            dict.pop(self, p.key, None)
            self.access_lookup.pop(p.key, None)
            num -= 1

    def _prune_invalidated_entries(self):
        ''''''

        self.access_log_lock.acquire()
        self.access_log = deque(e for e in self.access_log if e.is_valid)
        self.access_log_lock.release()

    def _get_ordered_access_keys(self):
        ''''''

        self.access_log_lock.acquire()
        r = [e.key for e in self.access_log if e.is_valid]
        self.access_log_lock.release()

        return r

    def __getitem__(self, key):
        item = dict.get(self, key)

        if not item:
            raise KeyError(key)

        ##

        ##

        self._push_entry(key)

        if len(self.access_log) > self.access_log_limit:
            ##

            ##

            self._prune_invalidated_entries()

        return item

    def __setitem__(self, key, item):
        ##

        dict.__setitem__(self, key, item)
        self._push_entry(key)

        ##

        self._prune_entries(len(self) - self._maxsize)

    def __delitem__(self, key):
        self._invalidate_entry(key)
        self.access_lookup.pop(key, None)
        dict.__delitem__(self, key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
