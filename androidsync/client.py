__all__ = [
    "Client"
]

from common import (
    make_python_identifier
)


class Client(object):

    def __init__(self, _id):
        self._id = _id
        self._all_sms = []

    def add_sms(self, *sms):
        for s in sms:
            self._all_sms.append(s)

    def __dfs_children__(self):
        return self._all_sms

    def __var_base__(self):
        return make_python_identifier(self._id)[0]

    def __gen_code__(self, g):
        g.gen_code(self)
        g.write(g.nameof(self) + ".add_sms(*")
        g.pprint(self._all_sms)
        g.line(")")
