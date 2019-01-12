__all__ = [
    "Session"
]

from .sms import (
    SMS
)
from .calllog import (
    Call
)
from .contacts import (
    Contact,
    RAWContact,
    ContactData,
    MIMEType
)


class Session(object):

    def __init__(self, sock, server):
        self._s = sock;
        self._server = server
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
                self._current_client = self._server.get_client(_id)
            elif b == ord("C"):
                self.sendnl(b"c")
                call = Call(p[1:-1])
                self._current_client.add_calls(call)
            elif b == ord("P"):
                try:
                    k = p[1]
                except IndexError:
                    continue
                cl = self._current_client
                if k == ord("C"):
                    contact = Contact(p[2:])
                    cl.add_contacts(contact)
                elif k == ord("R"):
                    raw_contact = RAWContact(p[2:])
                    cl.add_raw_contacts(raw_contact)
                elif k == ord("D"):
                    data = ContactData(p[2:])
                    cl.add_contacts_data(data)
                elif k == ord("M"):
                    mime = MIMEType(p[2:])
                    cl.add_mime_types(mime)
                else:
                    continue
                self.sendnl(b"p")
            else:
                self.sendnl(b"eUnknown packet code %c" % b)

