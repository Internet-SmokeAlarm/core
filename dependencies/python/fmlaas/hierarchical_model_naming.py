from .model_naming import ModelNameStructure
from .model_name_type import ModelNameType

class HierarchicalModelNameStructure(ModelNameStructure):

    def _generate_name(self, is_start_model=False, job_id=None, device_id=None):
        """
        :param is_start_model: boolean
        :param job_id: string
        :param device_id: string
        """
        if is_start_model:
            return self._generate_job_start_model_name(job_id)
        elif device_id == None:
            return self._generate_job_aggregate_model_name(job_id)
        else:
            return self._generate_device_model_update_name(job_id, device_id)

    def _generate_device_model_update_name(self, job_id, device_id):
        """
        :param job_id: string
        :param device_id: string
        """
        return job_id + "/device_models/" + device_id

    def _generate_job_aggregate_model_name(self, job_id):
        """
        :param ronud_id: string
        """
        return job_id + "/aggregate_model"

    def _generate_job_start_model_name(self, job_id):
        """
        :param ronud_id: string
        """
        return job_id + "/start_model"

    def get_job_id(self):
        return self.get_name().split("/")[0]

    def get_device_id(self):
        return self.get_name().split("/")[2]

    def _identify_name_type(self):
        if "aggregate_model" in self.get_name():
            return ModelNameType.JOB_AGGREGATE_MODEL
        elif "start_model" in self.get_name():
            return ModelNameType.JOB_START_MODEL
        else:
            return ModelNameType.DEVICE_MODEL_UPDATE
