__all__ = [
    "add_scrollbars"
]

from six.moves.tkinter import (
    HORIZONTAL,
    Scrollbar
)


def add_scrollbars(master, widget, w_row = 0, w_column = 0):
    master.rowconfigure(w_row + 1, weight = 0)
    master.columnconfigure(w_column + 1, weight = 0)

    vscroll = Scrollbar(master, command = widget.yview)
    vscroll.grid(row = w_row, column = w_column + 1, sticky = "NESW")

    hscroll = Scrollbar(master, command = widget.xview, orient = HORIZONTAL)
    hscroll.grid(row = w_row + 1, column = w_column, sticky = "NESW")

    widget.config(yscrollcommand = vscroll.set, xscrollcommand = hscroll.set)

    return vscroll, hscroll
