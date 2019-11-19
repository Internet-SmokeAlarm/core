from .db import DB

class InMemoryDBInterface(DB):

    ID_KEY_NAME = "ID"

    def __init__(self):
        self.data = {}

    def create_or_update_object(self, id, obj):
        self.data[id] = obj

        return True

    def delete_object(self, id):
        raise Exception("delete_object() not implemented")

    def get_object(self, id):
        if id not in self.data:
            raise Exception("Object not in DB")

        return self.data[id]
