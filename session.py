class Session(object):

    def __init__(self, sock):
        self._s = sock;

    def send(self, p):
        print("<< " + str(p))
        while p:
            sent = self._s.send(p)
            p=p[sent:]

    def recv(self):
        res = b""
        while True:
            p = self._s.recv(1024)
            if not p:
                break
            res += p
            if p[-1] == ord("\n"):
                break
        print(">> " + str(p))
        return p

    def run(self):
        p = self.recv()

        if not p:
            return

        for b in p:
            if b == ord("G"):
                self.send(b"g\n")
                return
