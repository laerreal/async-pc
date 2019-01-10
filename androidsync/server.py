__all__ = [
    "Server"
]

# qdt.common
from common import (
    notifier,
    pythonize
)
from .client import (
    Client
)
from .storage import (
    Storage
)


@notifier(
    "new_client" # client
)
class Server(object):

    def __init__(self):
        self._clients = {}

    def restore(self, file):
        s = Storage.load(file)
        self._clients = {}
        for c in s.clients:
            self._clients[c._id] = c

    def save(self, file):
        s = Storage(clients = self._clients)
        pythonize(s, file)

    def get_client(self, _id):
        try:
            client = self._clients[_id]
        except KeyError:
            client = Client(_id)
            self._clients[_id] = client
            self.__notify_new_client(client)
        return client
