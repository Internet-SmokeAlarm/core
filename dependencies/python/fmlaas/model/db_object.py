from abc import abstractmethod


class DBObject:

    @staticmethod
    def load_from_db(object_class, id, db_):
        """
        Load a specific instance from the DB.

        :param object_class: Class
        :param id: int
        :param db_: database
        """
        object = db_.get_object(id)

        return object_class.from_json(object)

    @abstractmethod
    def get_id(self):
        """
        :return: ID associated with DB object
        """
        raise NotImplementedError("get_id() not implemented")

    @abstractmethod
    def to_json(self):
        """
        :return: dict representation of self
        """
        raise NotImplementedError("to_json() not implemented")

    def save_to_db(self, db_):
        """
        :param db_: database
        """
        return db_.create_or_update_object(self.get_id(), self.to_json())
