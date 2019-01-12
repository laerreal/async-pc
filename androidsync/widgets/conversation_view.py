__all__ = [
    "ConversationView"
]

from six.moves.tkinter import (
    Toplevel,
    BOTH,
    Label,
    Text,
    Entry,
    WORD,
    DISABLED,
    Frame,
    END
)
from .double_scrollbar_frame import (
    DoubleScrollbarFrame
)
from .text_helpers import (
    adjust_text_height
)


# TODO: this class is same as SMSView
class ConversationView(DoubleScrollbarFrame):

    def __init__(self, conv, *a, **kw):
        DoubleScrollbarFrame.__init__(self, *a, **kw)

        self._inner = inner = Frame(self.canvas)
        self._inner_id = self.canvas.create_window((0, 0),
            window = inner, anchor = "nw"
        )
        inner.bind("<Configure>", self._on_inner_configure)
        self.canvas.bind("<Configure>", self._on_configure)

        inner.columnconfigure(0, weight = 1)
        inner.rowconfigure(0, weight = 1)

        self._next_row = 0

        self._conv = conv

        self._s_conv = s_conv = sorted(conv, key = lambda i : i["date"])

        for item in s_conv:
            if item.incomming:
                sticky = "NWS"
            else:
                sticky = "NES"

            e = self._append(Entry)
            e.insert(END, item.datetime.strftime("%Y.%m.%d %H:%M:%S"))
            e.config(state = "readonly")
            e.grid(sticky = sticky)

            t = self._append(Text, wrap = WORD)
            t.grid(sticky = "NESW")
            t.insert(END, item.message)
            t.config(state = DISABLED)

    def _append(self, wcls, *a, **kw):
        inner = self._inner

        inner.rowconfigure(self._next_row, weight = 0)

        w = wcls(inner, *a, **kw)
        w.grid(row = self._next_row + 1, column = 0)

        self._next_row += 1
        return w

    def _on_configure(self, e):
        self.canvas.itemconfig(self._inner_id, width = e.width)

        for w in self._inner.winfo_children():
            if isinstance(w, Text):
                adjust_text_height(w)

    def _on_inner_configure(self, _):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
