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

        return self

    def generate_name(self, is_start_model=False, job_id=None, device_id=None):
        """
        :param is_start_model: boolean
        :param device_id: string
        :param job_id: string
        """
        self.name = self._generate_name(is_start_model=is_start_model, job_id=job_id, device_id=device_id)
        self.name_type = self._identify_name_type()

    @abstractmethod
    def _identify_name_type(self):
        """
        :returns: ModelNameType
        """
        raise NotImplementedError("_identify_name_type() not implemented")

    def is_job_aggregate_model(self):
        return self.get_name_type() == ModelNameType.JOB_AGGREGATE_MODEL

    def is_job_start_model(self):
        return self.get_name_type() == ModelNameType.JOB_START_MODEL

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
    def get_job_id(self):
        """
        :returns: int
        """
        raise NotImplementedError("get_job_id() not implemented")

    @abstractmethod
    def get_device_id(self):
        """
        :returns: int
        """
        raise NotImplementedError("get_device_id() not implemented")

    @abstractmethod
    def _generate_name(self, is_start_model=False, job_id=None, device_id=None):
        """
        Generates appropriate S3 object name given information.

        :param device_id: string
        :param job_id: string
        :param is_start_model: boolean
        """
        raise NotImplementedError("_generate_name() not implemented")
