__all__ = [
    "Server"
]

from qdt.common import (
    pythonize
)
from .client import (
    Client
)
from .storage import (
    Storage
)


class Server(object):

    def __init__(self):
        self._clients = {}

    def restore(self, file):
        s = Storage.load(file)
        self._clients = {} if s.clients is None else s.clients

    def save(self, file):
        s = Storage(clients = self._clients)
        pythonize(s, file)

    def get_client(self, _id):
        try:
            client = self._clients[_id]
        except KeyError:
            client = Client(_id)
            self._clients[_id] = client
        return client
