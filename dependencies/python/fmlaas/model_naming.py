from abc import abstractmethod

class ModelNameStructure:

    def __init__(self):
        self.name = None

    def load_name(self, object_name):
        """
        :param object_name: string
        """
        self.name = object_name

    def generate_name(self, group_id, round_id, device_id):
        """
        :param device_id: string
        :param round_id: string
        :param group_id: string
        """
        self.name = self._generate_model_object_name(group_id, round_id, device_id)

    def get_name(self):
        return self.name

    @abstractmethod
    def get_group_id(self):
        """
        :returns: int
        """
        raise NotImplementedError("get_group_id() not implemented")

    @abstractmethod
    def get_round_id(self):
        """
        :returns: int
        """
        raise NotImplementedError("get_round_id() not implemented")

    @abstractmethod
    def get_device_id(self):
        """
        :returns: int
        """
        raise NotImplementedError("get_device_id() not implemented")

    @abstractmethod
    def _generate_model_object_name(self, group_id, round_id, device_id):
        """
        Generates appropriate S3 object name given information.

        :param device_id: string
        :param round_id: string
        :param group_id: string
        """
        raise NotImplementedError("generate_model_object_name() not implemented")
