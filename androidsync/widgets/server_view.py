__all__ = [
    "ServerView"
]

from six.moves.tkinter import (
    Frame
)
from six.moves.tkinter.ttk import  (
    Notebook
)
from .client_view import (
    ClientView
)


class ServerView(Frame):

    def __init__(self, server, *a, **kw):
        Frame.__init__(self, *a, **kw)

        self._srv = server

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self._nb = nb = Notebook(self)
        nb.grid(row = 0, column = 0, sticky = "NESW")

        self._clients2tabs = {}

        self._update_tabs()

        server.watch_new_client(self._on_new_client)

    def _update_tabs(self):
        nb = self._nb
        rest = dict(self._srv._clients)

        # remove tabs for removed clients
        for tab_id in tuple(nb.tabs()):
            c_id = nb.tab(tab_id, option = "text")
            if rest.pop(c_id, None) is None:
                self.nb.forget(tab_id)

        for c_id, client in rest.items(): # new clients only left
            c_view = ClientView(client, nb)
            nb.add(c_view, text = c_id)

    def _on_new_client(self, *_):
        self._update_tabs()
