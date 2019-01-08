from os.path import (
    isfile,
    join,
    dirname
)
from socket import (
    socket,
    SOCK_STREAM,
    AF_INET
)
from os import (
    remove,
    rename
)
from androidsync import (
    Server,
    Session
)


import sys

sys.path.insert(0, join(dirname(__file__), join("deps", "pyrsp")))

from pyrsp.utils import (
    find_free_port
)

STATE_FILE = "_session_state.py"

if __name__ == "__main__":
    print("ASync PC (server) application")

    srv = Server()
    srv.restore(STATE_FILE)

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

        srv.save("_tmp" + STATE_FILE)

        if isfile(STATE_FILE):
            remove(STATE_FILE)
        rename("_tmp" + STATE_FILE, STATE_FILE)

        try: cs.close();
        except: pass
