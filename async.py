from os.path import (
    join,
    dirname
)
from socket import (
    socket,
    SOCK_STREAM,
    AF_INET
)

from session import (
    Session
)
from client import (
    Client
)

import sys

sys.path.insert(0, join(dirname(__file__), join("deps", "pyrsp")))

from pyrsp.utils import (
    find_free_port
)


class Server(object):

    def __init__(self):
        self._clients = {}

    def get_client(self, _id):
        try:
            client = self._clients[_id]
        except KeyError:
            client = Client(_id)
            self._clients[_id] = client
        return client


if __name__ == "__main__":
    print("ASync PC (server) application")

    srv = Server()

    port = find_free_port()

    ss = socket(AF_INET, SOCK_STREAM)
    # ss.bind(("127.0.0.1", port)) # accept from localhost only
    ss.bind(("", port)) # listen an all ports

    working = True

    while working:
        ss.listen(10)
        print("Listening %s" % port)
        cs, remote = ss.accept()
        print("Connection from %s:%u" % remote)
        s = Session(cs, srv)

        s.run();

        try: cs.close();
        except: pass
