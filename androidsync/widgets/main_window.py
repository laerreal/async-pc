__all__ = [
    "MainWindow"
]

from six.moves.tkinter import (
    PhotoImage,
    Tk
)
from .server_view import (
    ServerView
)
from os.path import (
    dirname,
    join
)


class MainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.title("Android Synchronizer")

        try:
            ico = PhotoImage(file = join(dirname(__file__), "logo.gif"))
            self.tk.call("wm", "iconphoto", self._w, ico)
        except Exception as e:
            print("Failed to set icon: %s" % e)

        self._server = None

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, srv):
        if self._server is not None:
            self._srv_view.destroy()

        self._server = srv
        self._srv_view = sv = ServerView(srv, self)

        sv.grid(row = 0, column = 0, sticky = "NESW")
