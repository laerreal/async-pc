__all__ = [
    "SMSView",
    "SMSWindow"
]


from six.moves.tkinter import (
    Toplevel,
    BOTH,
    Label,
    Text,
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


class SMSView(DoubleScrollbarFrame):

    def __init__(self, sms, *a, **kw):
        DoubleScrollbarFrame.__init__(self, *a, **kw)

        self._inner = inner = Frame(self.canvas)
        self._inner_id = self.canvas.create_window((0, 0),
            window = inner, anchor = "nw"
        )
        inner.bind("<Configure>", self._on_inner_configure)
        self.canvas.bind("<Configure>", self._on_configure)

        inner.columnconfigure(0, weight = 1)

        self._next_row = 0

        rest = dict(sms.json)

        message = sms.message
        rest.pop("body")

        self._append('Message (UTF-8 decoded "body")', message)

        while rest:
            k, v = rest.popitem()
            self._append(k, v)

    def _append(self, heading, content):
        inner = self._inner

        inner.rowconfigure(self._next_row, weight = 0)
        inner.rowconfigure(self._next_row + 1, weight = 1)

        Label(inner, text = heading).grid(
            row = self._next_row, column = 0, sticky = "NSW"
        )
        t = Text(inner, wrap = WORD)
        t.grid(row = self._next_row + 1, column = 0, sticky = "NESW")
        t.insert(END, content)
        t.config(state = DISABLED)

        self._next_row += 2

    def _on_configure(self, e):
        self.canvas.itemconfig(self._inner_id, width = e.width)

        for w in self._inner.winfo_children():
            if isinstance(w, Text):
                adjust_text_height(w)

    def _on_inner_configure(self, _):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))


class SMSWindow(Toplevel):

    def __init__(self, sms):
        Toplevel.__init__(self)

        self._sms = sms

        self.title("SMS from %s" % sms["address"])

        v = SMSView(sms, self)
        v.pack(fill = BOTH, expand = True)
