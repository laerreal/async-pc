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


def add_raw_unique(container, *items):
    added = False
    for i in items:
        h = hash(i._raw)
        if h not in container:
            added = True
            container[h] = i
    return added


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
        self._contacts = {}
        self._raw_contacts = {}
        self._contacts_data = {}
        self._mime_types = {}

    def add_sms(self, *sms):
        # prevent duplication using raw SMS as hash
        if add_raw_unique(self._all_sms, *sms):
            self.__notify_sms_added()

        return self

    def add_calls(self, *calls):
        add_raw_unique(self._all_calls, *calls)
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
