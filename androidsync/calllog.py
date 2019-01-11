__all__ = [
    "Call"
]

from .json_originated import (
    JSONOriginated
)


class Call(JSONOriginated):

    def __var_base__(self):
        return "call"
