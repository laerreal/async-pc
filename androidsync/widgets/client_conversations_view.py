__all__ = [
    "ClientConversationsView"
]

from six.moves.tkinter import (
    BOTH,
    TRUE,
    Frame
)
from .invalidate import (
    Invalidate
)
from six.moves.tkinter.ttk import (
    Treeview
)
from .scrollbars import (
    add_scrollbars
)
from .conversation_view import (
    ConversationView
)


class ClientConversationsView(Frame, Invalidate):

    def __init__(self, client, *a, **kw):
        Frame.__init__(self, *a, **kw)

        self._client = client

        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        self._addresses_w = a_w = Frame(self, width = 100)
        a_w.grid(row = 0, column = 0, sticky = "NESW")

        a_w.rowconfigure(0, weight = 1)
        a_w.columnconfigure(0, weight = 1)

        self._addresses_tv = a_tv = Treeview(a_w, columns = ("address",))
        a_tv.heading("#0", text = "#")
        a_tv.heading("address", text = "Sender")
        a_tv.column("#0", minwidth = 50, width = 50)
        a_tv.column("address", minwidth = 100, width = 100)

        a_tv.grid(row = 0, column = 0, sticky = "NESW")
        add_scrollbars(a_w, a_tv)

        a_tv.bind("<<TreeviewSelect>>", self._on_address_tv_select)

        self.columnconfigure(1, weight = 10)

        # ConversationView(DoubleScrollbarFrame) uses `pack` layout manager.
        # This frame handles this.
        self._conversation_w_holder = conv_w = Frame(self)
        conv_w.grid(row = 0, column = 1, sticky = "NESW")

        self._invalidate()
        client.watch_sms_added(self._on_sms_added)

    def _update(self):
        self._conversations = convs = self._client.get_conversations()

        a_tv = self._addresses_tv

        prev_sel = a_tv.selection()
        if prev_sel:
            sel_addr = a_tv.item(prev_sel, "tags")[0]
        else:
            sel_addr = None

        # XXX: a dark side of power
        a_tv.delete(*a_tv.get_children())

        # Sorting:
        # - address's time is time of its last message
        # - most recent address to the top (lowest index)
        for conv in convs.values():
            conv.sort(key = lambda item : item["date"])

        s_convs = sorted(convs.keys(), key = lambda a : convs[a][-1]["date"])

        sel_iid = None
        for i, addr in enumerate(reversed(s_convs)):
            iid = a_tv.insert("", "end",
                text = str(i),
                values = (addr,),
                tags = (addr,)
            )

            if sel_iid is None:
                sel_iid = iid
            elif addr == sel_addr:
                sel_iid = iid

        if convs:
            a_tv.selection_set(sel_iid)

    def _on_address_tv_select(self, _):
        # TODO: the selection can be same
        for w in self._conversation_w_holder.winfo_children():
            w.destroy()

        item = self._addresses_tv.selection()[0]
        addr = self._addresses_tv.item(item, "tags")[0]
        conv = self._conversations[addr]

        conv_w = ConversationView(conv, self._conversation_w_holder)
        conv_w.pack(fill = BOTH, expand = TRUE)


    def _on_sms_added(self):
        self._invalidate()
