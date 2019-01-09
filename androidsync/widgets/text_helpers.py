__all__ = [
    "adjust_text_height"
]

def adjust_text_height(t):
    "Given Tkinter Text widget tries to set its height to fit all the text."

    def cb(t = t):
        t.see("end")

        # get number of a line at top by index of character at (3px, 3px)
        top_line, char = t.index("@3,3").split(".")

        # print("char = " + char)
        if char != "0":
            # the top line is displayed from its middle
            # TODO: estimate number of hidden rows more precisely
            top_line_hidden_rows = 2
        else:
            top_line_hidden_rows = 0

        # get number of rows occupied by all displayed text
        _, y, _, h = t.bbox("end-1c")
        bottom_rows = (y + h) // h

        # print((top_line_hidden_rows, int(top_line), bottom_rows))

        height = top_line_hidden_rows + (int(top_line) - 1) + bottom_rows
        t.configure(height = height)

    t.after(100, cb)
