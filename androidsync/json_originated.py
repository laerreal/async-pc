__all__ = [
    "JSONOriginated"
]

from six import (
    PY3
)
from json import (
    loads
)
# qdt.common
from common import (
    lazy
)


class JSONOriginated(object):

    def __init__(self, _raw):
        if PY3 and isinstance(_raw, bytes):
            # this encoding is quite fast and supports all byte values [0;255]
            _raw = _raw.decode("charmap")

        self._raw = _raw;

    @lazy
    def json(self):
        return loads(self._raw)

    def __getitem__(self, name):
        return self.json[name]

    def __str__(self):
        return str(self._raw)

    __gen_code__ = lambda self, g : g.gen_code(self)
