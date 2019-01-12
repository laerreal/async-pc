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
from base64 import (
    b64decode
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
        val = self.json[name]
        if (isinstance(val, dict)
            and tuple(sorted(val.keys())) == ("data", "encoding")
        ):
            if val["encoding"] == "base64":
                val = b64decode(val["data"]).decode("charmap")
        return val

    def __str__(self):
        return str(self._raw)

    __gen_code__ = lambda self, g : g.gen_code(self)
