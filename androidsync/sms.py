__all__ = [
    "SMS",

    "MESSAGE_TYPE"
    # MESSAGE_TYPE_* are exported programmically
]

from .json_originated import (
    JSONOriginated
)
from common import (
    lazy
)
from six import (
    PY3
)
from datetime import (
    datetime
)
fromtimestamp = datetime.fromtimestamp

# See:
# https://developer.android.com/reference/kotlin/android/provider/Telephony.TextBasedSmsColumns

# column name
MESSAGE_TYPE = "type"

TYPES = dict(
    MESSAGE_TYPE_ALL = "0",
    MESSAGE_TYPE_INBOX = "1",
    MESSAGE_TYPE_SENT = "2",
    MESSAGE_TYPE_DRAFT = "3",
    MESSAGE_TYPE_OUTBOX = "4",
    MESSAGE_TYPE_FAILED = "5",
    MESSAGE_TYPE_QUEUED = "6"
)

for t, v in TYPES.items():
    globals()[t] = v
    __all__.append(t)

TYPES.update(tuple((v, t) for t, v in TYPES.items()))


class SMS(JSONOriginated):

    @lazy
    def datetime(self):
        epoch_ms = int(self["date"])
        return fromtimestamp(epoch_ms / 1000.0)

    @lazy
    def incoming(self):
        return self["type"] == MESSAGE_TYPE_INBOX

    @lazy
    def message(self):
        res = self["body"].encode("charmap").decode("utf-8")
        return res

    @lazy
    def line(self):
        res = self.message.replace("\n", " ")
        return res

    @lazy
    def headings(self):
        return tuple(self.json.keys())

    def __str__(self):
        return str(self._raw)

    def __var_base__(self):
        return "sms"
