import storage_names


class Storage(object):

    def __init__(self, clients = None):
        self.clients = clients if clients else None

    def __var_base__(self):
        return "storage"

    def __dfs_children__(self):
        return tuple(self.clients.values())

    def __gen_code__(self, g):
        g.gen_code(self)

    @classmethod
    def load(cls, file):
        namespace = {"Storage": cls}
        namespace.update(storage_names.__dict__)
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
