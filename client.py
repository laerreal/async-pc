class Client(object):

    def __init__(self, _id):
        self._id = _id
        self._all_sms = []

    def add_sms(self, sms):
        self._all_sms.append(sms)
