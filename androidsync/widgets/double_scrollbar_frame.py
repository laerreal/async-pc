__all__ = [
    "DoubleScrollbarFrame"
]

# Based on
# https://lucasg.github.io/2015/07/21/How-to-make-a-proper-double-scrollbar-frame-in-Tkinter/

from six.moves.tkinter import (
    Frame,
    Canvas,
    HORIZONTAL,
    VERTICAL,
    BOTTOM,
    RIGHT,
    LEFT,
    TRUE,
    FALSE,
    BOTH,
    X,
    Y
)
from six.moves.tkinter.ttk import (
    Scrollbar,
    Sizegrip
)


class DoubleScrollbarFrame(Frame):

    def __init__(self, master, **kwargs):
        '''
          Initialisation. The DoubleScrollbarFrame consist of :
            - an horizontal scrollbar
            - a  vertical   scrollbar
            - a canvas in which the user can place sub-elements
        '''

        Frame.__init__(self, master, **kwargs)

        # Canvas creation with double scrollbar
        self.hscrollbar = Scrollbar(self, orient = HORIZONTAL)
        self.vscrollbar = Scrollbar(self, orient = VERTICAL)
        self.sizegrip = Sizegrip(self)
        self.canvas = Canvas(self, bd = 0, highlightthickness = 0,
                                      yscrollcommand = self.vscrollbar.set,
                                      xscrollcommand = self.hscrollbar.set)
        self.vscrollbar.config(command = self.canvas.yview)
        self.hscrollbar.config(command = self.canvas.xview)

    def pack(self, **kwargs):
        '''
          Pack the scrollbar and canvas correctly in order to recreate the
          same look as MFC's windows.
        '''

        self.hscrollbar.pack(side = BOTTOM, fill = X, expand = FALSE)
        self.vscrollbar.pack(side = RIGHT, fill = Y, expand = FALSE)
        self.sizegrip.pack(in_ = self.hscrollbar, side = BOTTOM, anchor = "se")
        self.canvas.pack(
            side = LEFT,
            padx = 5, pady = 5,
            fill = BOTH, expand = TRUE
        )

        Frame.pack(self, **kwargs)
