__all__ = [
    "Storage"
]

import androidsync


class Storage(object):

    def __init__(self, clients = None):
        if isinstance(clients, dict): # old format
            clients = tuple(clients.values())
        elif not isinstance(clients, tuple):
            clients = clients if clients else ()

        self.clients = clients

    def __var_base__(self):
        return "storage"

    def __dfs_children__(self):
        return self.clients

    def __gen_code__(self, g):
        g.gen_code(self)

    @classmethod
    def load(cls, file):
        namespace = {"Storage": cls}
        namespace.update(androidsync.__dict__)
        result = {}
        try:
            with open(file, "r") as f:
                source = f.read()
        except Exception as e:
            print(str(e))
            source = ""

        try:
            exec(source, namespace, result)
        except Exception as e:
            print("State loading failed: " + str(e))
        for n in result.values():
            if isinstance(n, cls):
                return n
        return Storage()
