from os.path import (
    isfile,
    join,
    dirname
)
from socket import (
    timeout as SocketTimeout,
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
from widgets import (
    MainWindow
)
from threading import (
    Thread
)


import sys

sys.path.insert(0, join(dirname(__file__), join("deps", "pyrsp")))

from pyrsp.utils import (
    find_free_port
)

STATE_FILE = "_session_state.py"


def net_thread_func(srv):
    global working

    ss = socket(AF_INET, SOCK_STREAM)
    ss.settimeout(1.0)
    # ss.bind(("127.0.0.1", port)) # accept from localhost only
    ss.bind(("", port)) # listen an all ports

    while working:
        ss.listen(10)
        print("Listening %s" % port)

        while working:
            try:
                cs, remote = ss.accept()
            except SocketTimeout:
                continue
            else:
                break
        else:
            continue

        print("Connection from %s:%u" % remote)
        s = Session(cs, srv)

        s.run();

        srv.save("_tmp" + STATE_FILE)

        if isfile(STATE_FILE):
            remove(STATE_FILE)
        rename("_tmp" + STATE_FILE, STATE_FILE)

        try: cs.close();
        except: pass


if __name__ == "__main__":
    print("ASync PC (server) application")

    srv = Server()
    srv.restore(STATE_FILE)

    port = find_free_port()

    global working
    working = True

    net_thread = Thread(target = net_thread_func, args = (srv,))
    net_thread.start()

    root = MainWindow()
    root.server = srv

    def on_wm_delete_window():
        global working
        working = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_wm_delete_window)

    root.mainloop()

    net_thread.join()
