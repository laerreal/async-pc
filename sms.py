class SMS(object):
    def __init__(self, raw):
        self._raw = raw;

    def __str__(self):
        return str(self._raw)
