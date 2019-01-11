__all__ = [
    "ConversationView"
]

from six.moves.tkinter import (
    Text,
    RIGHT,
    WORD,
    DISABLED,
    Frame,
    END
)
from .scrollbars import (
    add_scrollbars
)

class ConversationView(Frame):

    def __init__(self, conv, *a, **kw):
        Frame.__init__(self, *a, **kw)

        self._conv = conv
        self._s_conv = s_conv = sorted(conv, key = lambda i : i["date"])

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)

        self._text = text = Text(self, wrap = WORD)
        text.grid(row = 0, column = 0, sticky = "NESW")

        add_scrollbars(self, text)

        # incoming
        text.tag_config("itime",
            foreground = "grey",
            background = "#eeeeee",
            selectbackground = "SystemHighlight",
            selectforeground = "SystemHighlightText"
        )
        text.tag_config("imessage",
            rmargin = 100
        )

        text.tag_config("otime",
            justify = RIGHT,
            foreground = "grey",
            background = "#eeeeee",
            selectbackground = "SystemHighlight",
            selectforeground = "SystemHighlightText"
        )
        text.tag_config("omessage",
            lmargin1 = 100,
            lmargin2 = 100,
            background = "#f8f8f8",
            selectbackground = "SystemHighlight",
        )

        for item in s_conv:
            prefix = "i" if item.incoming else "o"

            text.insert(END,
                item.datetime.strftime("%Y.%m.%d %H:%M:%S") + "\n",
                prefix + "time"
            )
            text.insert(END, item.message + "\n\n", prefix + "message")

        text.config(state = DISABLED)
        text.see("end-1c")
