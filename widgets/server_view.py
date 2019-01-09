__all__ = [
    "ServerView"
]

from six.moves.tkinter import (
    Frame
)
from six.moves.tkinter.ttk import  (
    Notebook
)


class ServerView(Frame):

    def __init__(self, server, *a, **kw):
        Frame.__init__(self, *a, **kw)

        self._srv = server

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self._nb = nb = Notebook(self)
        nb.grid(row = 0, column = 0, sticky = "NESW")

        self._sms_w = sms_w = Frame(nb)
        nb.add(sms_w, text = "SMS")

        self._calls_w = calls_w = Frame(nb)
        nb.add(calls_w, text = "Calls")
