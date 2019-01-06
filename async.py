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

import sys

sys.path.insert(0, join(dirname(__file__), join("deps", "pyrsp")))

from pyrsp.utils import (
    find_free_port
)

if __name__ == "__main__":
    print("ASync PC (server) application")

    port = find_free_port()

    ss = socket(AF_INET, SOCK_STREAM)
    ss.bind(("127.0.0.1", port))

    working = True

    while working:
        ss.listen(10)
        print("Listening %s" % port)
        cs, remote = ss.accept()
        print("Connection from %s:%u" % remote)
        s = Session(cs)

        s.run();

        try: cs.close();
        except: pass
