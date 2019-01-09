__all__ = [
    "Client"
]

from common import (
    make_python_identifier
)
from itertools import (
    chain
)


class Client(object):

    def __init__(self, _id):
        self._id = _id
        self._all_sms = {}
        self._all_calls = {}

    def add_sms(self, *sms):
        for s in sms:
            # prevent duplication using raw SMS as hash
            self._all_sms[hash(s._raw)] = s
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
