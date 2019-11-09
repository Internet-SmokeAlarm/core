from abc import abstractmethod
from abc import ABC

class DB(ABC):

    @abstractmethod
    def create_or_update_object(self, id, obj):
        """
        :param id: object id to create/update from db
        :param obj: json object to create/update in db
        :returns: true/false if operation successful
        """
        raise Exception("create_or_update_object() not implemented")

    @abstractmethod
    def delete_object(self, id):
        """
        :param id: object id to delete from db
        :returns: true/false if operation successful
        """
        raise Exception("delete_object() not implemented")

    @abstractmethod
    def get_object(self, id):
        """
        :param id: object id to retrieve from db
        :returns: json of object
        """
        raise Exception("get_object() not implemented")
