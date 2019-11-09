from .db import DB
from ..aws import get_dynamodb_table

class DynamoDBInterface(DB):

    ID_KEY_NAME = "ID"

    def __init__(self, table_name):
        self.table = get_dynamodb_table(table_name)

    def create_or_update_object(self, id, obj):
        """
        :param id: object id to create/update from db
        :param obj: json object to create/update in db
        :returns: true/false if operation successful
        """
        return self.table.put_item(Item={
            DynamoDBInterface.ID_KEY_NAME : id,
            **obj
        })

    def delete_object(self, id):
        """
        :param id: object id to delete from db
        :returns: true/false if operation successful
        """
        raise Exception("delete_object() not implemented")

    def get_object(self, id):
        """
        :param id: object id to retrieve from db
        :returns: json of object
        """
        return self.table.get_item(Key={
            DynamoDBInterface.ID_KEY_NAME : id
        })["Item"]
