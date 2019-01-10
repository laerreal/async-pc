__all__ = [
    "ClientView"
]

from six.moves.tkinter import (
    Frame
)
from six.moves.tkinter.ttk import (
    Treeview,
    Notebook
)
from .scrollbars import (
    add_scrollbars
)
from .sms_view import (
    SMSWindow
)


class ClientView(Frame):

    def __init__(self, client, *a, **kw):
        Frame.__init__(self, *a, **kw)

        self._client = client

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self._nb = nb = Notebook(self)
        nb.grid(row = 0, column = 0, sticky = "NESW")

        self._sms_w = sms_w = Frame(nb)
        nb.add(sms_w, text = "SMS")

        sms_w.rowconfigure(0, weight = 1)
        sms_w.columnconfigure(0, weight = 1)

        self._sms_tv = sms_tv = Treeview(sms_w, columns = ("address", "body"))
        sms_tv.heading("#0", text = "#")
        sms_tv.heading("address", text = "Sender")
        sms_tv.heading("body", text = "Message")
        sms_tv.column("#0", minwidth = 50)
        sms_tv.column("address", minwidth = 100)
        sms_tv.column("body", minwidth = 500)

        sms_tv.grid(row = 0, column = 0, sticky = "NESW")

        add_scrollbars(sms_w, sms_tv)

        sms_tv.bind("<Double-1>", self._on_double_1)

        self._calls_w = calls_w = Frame(nb)
        nb.add(calls_w, text = "Calls")

        self._invalidate()

        client.watch_sms_added(self._on_sms_added)

    def _update(self):
        sms_tv = self._sms_tv

        # XXX: a dark side of power
        sms_tv.delete(*sms_tv.get_children())

        all_sms = list(self._client._all_sms.items())

        s_all_sms = sorted(all_sms, key = lambda h_sms : int(h_sms[1]["date"]))

        for i, (_hash, sms) in enumerate(s_all_sms):
            sms_tv.insert("", "end",
                text = str(i),
                values = (sms["address"], sms.line),
                tags = (str(_hash),)
            )

    def _on_double_1(self, _):
        item = self._sms_tv.selection()[0]
        sms = self._client._all_sms[int(self._sms_tv.item(item, "tags")[0])]

        SMSWindow(sms).geometry("500x600")

    def _invalidate(self):
        if hasattr(self, "_after_update_id"):
            return
        self._after_update_id = self.after(100, self._after_update)

    def _after_update(self):
        del self._after_update_id
        self._update()

    def _on_sms_added(self):
        self._invalidate()
