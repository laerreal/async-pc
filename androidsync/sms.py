__all__ = [
    "SMS"
]


class SMS(object):

    def __init__(self, _raw):
        self._raw = _raw;

    def __str__(self):
        return str(self._raw)

    def __var_base__(self):
        return "sms"

    def __gen_code__(self, g):
        g.gen_code(self)
