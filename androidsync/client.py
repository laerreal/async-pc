__all__ = [
    "Client"
]

# qdt.common
from common import (
    notifier
)
from .common import (
    make_python_identifier
)
from itertools import (
    chain
)
from collections import (
    defaultdict
)


@notifier("sms_added")
class Client(object):

    def __init__(self, _id):
        """
:type _id: str
:param _id: Human readable identifier of client.
        """
        self._id = _id
        self._all_sms = {}
        self._all_calls = {}

    def add_sms(self, *sms):
        _all = self._all_sms
        added = False
        for s in sms:
            # prevent duplication using raw SMS as hash
            h = hash(s._raw)
            if h in _all:
                continue
            added = True
            _all[h] = s

        if added:
            self.__notify_sms_added()

        return self

    def add_calls(self, *calls):
        for c in calls:
            self._all_calls[hash(c._raw)] = c
        return self

    def __dfs_children__(self):
        return tuple(chain(self._all_sms.values(), self._all_calls.values()))

    def __var_base__(self):
        return make_python_identifier(self._id)[0]

    def __gen_code__(self, g):
        g.gen_code(self)
        g.write(g.nameof(self) + ".add_sms(*")
        g.pprint(tuple(self._all_sms.values()))
        g.line(")")
        g.write(g.nameof(self) + ".add_calls(*")
        g.pprint(tuple(self._all_calls.values()))
        g.line(")")

    def get_conversations(self):
        addresses = defaultdict(list)
        for sms in self._all_sms.values():
            addresses[sms["address"]].append(sms)
        return addresses
