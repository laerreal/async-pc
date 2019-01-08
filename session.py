from sms import (
    SMS
)
from client import (
    Client
)

class Session(object):

    def __init__(self, sock):
        self._s = sock;
        self._clients = {}
        # self._current_client = None # it's better to raise AttributeError

    def send(self, p):
        print("<< " + str(p))
        while p:
            sent = self._s.send(p)
            p=p[sent:]

    def sendnl(self, l):
        self.send(l + b"\n")

    def recv(self):
        res = b""
        while True:
            p = self._s.recv(1024)
            if not p:
                break
            print(">> " + str(p))
            res += p
            if p[-1] == ord("\n"):
                break
        return res

    def run(self):
        while True:
            p = self.recv()

            if not p:
                return

            b = p[0]
            if b == ord("G"):
                self.send(b"g\n")
                return
            elif b == ord("S"):
                sms = SMS(p[1:-1])
                self._current_client.add_sms(sms)
                self.sendnl(b"s")
                # print("%s" % sms)
            elif b == ord("I"):
                _id = p[1:-1].decode("utf-8")
                self.sendnl(b"i")
                try:
                    client = self._clients[_id]
                except KeyError:
                    client = Client(_id)
                    self._clients[_id] = client
                self._current_client = client
            else:
                self.sendnl(b"eUnknown packet code %c" % b)

