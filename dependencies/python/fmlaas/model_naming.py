from abc import abstractmethod
from .model_name_type import ModelNameType

class ModelNameStructure:

    def __init__(self):
        self.name = None
        self.name_type = None

    def load_name(self, object_name):
        """
        :param object_name: string
        """
        self.name = object_name
        self.name_type = self._identify_name_type()

    def generate_name(self, group_id=None, round_id=None, device_id=None):
        """
        :param device_id: string
        :param round_id: string
        :param group_id: string
        """
        self.name = self._generate_model_object_name(group_id=group_id, round_id=round_id, device_id=device_id)
        self.name_type = self._identify_name_type()

    @abstractmethod
    def _identify_name_type(self):
        """
        :returns: ModelNameType
        """
        raise NotImplementedError("_identify_name_type() not implemented")

    def is_round_aggregate_model(self):
        return self.get_name_type() == ModelNameType.ROUND_AGGREGATE_MODEL

    def is_initial_group_model(self):
        return self.get_name_type() == ModelNameType.INITIAL_GROUP_MODEL

    def is_device_model_update(self):
        return self.get_name_type() == ModelNameType.DEVICE_MODEL_UPDATE

    def get_name_type(self):
        """
        :returns: ModelNameType
        """
        return self.name_type

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
    def _generate_model_object_name(self, group_id=None, round_id=None, device_id=None):
        """
        Generates appropriate S3 object name given information.

        :param device_id: string
        :param round_id: string
        :param group_id: string
        """
        raise NotImplementedError("_generate_model_object_name() not implemented")
