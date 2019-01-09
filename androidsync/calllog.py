__all__ = [
    "Call"
]

class Call(object):

    def __init__(self, _raw):
        self._raw = _raw

    def __str__(self):
        return str(self._raw)

    def __var_base__(self):
        return "call"

    __gen_code__ = lambda self, g : g.gen_code(self)
