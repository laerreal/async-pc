__all__ = [
    "SMS"
]

from json import (
    loads
)
from common import (
    lazy
)
from six import (
    PY3
)


class SMS(object):

    def __init__(self, _raw):
        if PY3 and isinstance(_raw, bytes):
            # this encoding is quite fast and supports all byte values [0;255]
            _raw = _raw.decode("charmap")

        self._raw = _raw;

    @lazy
    def message(self):
        res = self["body"].encode("charmap").decode("utf-8")
        return res

    @lazy
    def line(self):
        res = self.message.replace("\n", " ")
        return res

    @lazy
    def json(self):
        return loads(self._raw)

    @lazy
    def headings(self):
        return tuple(self.json.keys())

    def __getitem__(self, name):
        return self.json[name]

    def __str__(self):
        return str(self._raw)

    def __var_base__(self):
        return "sms"

    def __gen_code__(self, g):
        g.gen_code(self)
