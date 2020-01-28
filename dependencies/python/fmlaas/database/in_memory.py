from .db import DB

class InMemoryDBInterface(DB):

    ID_KEY_NAME = "ID"

    def __init__(self):
        self.data = {}

    def create_or_update_object(self, id, obj):
        self.data[id] = obj

        return True

    def delete_object(self, id):
        del self.data[id]

    def get_object(self, id):
        return self.data[id]
