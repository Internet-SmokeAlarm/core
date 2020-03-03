from .model_naming import ModelNameStructure
from .model_name_type import ModelNameType

class HierarchicalModelNameStructure(ModelNameStructure):

    def _generate_name(self, is_start_model=False, round_id=None, device_id=None):
        """
        :param is_start_model: boolean
        :param round_id: string
        :param device_id: string
        """
        if is_start_model:
            return self._generate_round_start_model_name(round_id)
        elif device_id == None:
            return self._generate_round_aggregate_model_name(round_id)
        else:
            return self._generate_device_model_update_name(round_id, device_id)

    def _generate_device_model_update_name(self, round_id, device_id):
        """
        :param round_id: string
        :param device_id: string
        """
        return round_id + "/device_models/" + device_id

    def _generate_round_aggregate_model_name(self, round_id):
        """
        :param ronud_id: string
        """
        return round_id + "/aggregate_model"

    def _generate_round_start_model_name(self, round_id):
        """
        :param ronud_id: string
        """
        return round_id + "/start_model"

    def get_round_id(self):
        return self.get_name().split("/")[0]

    def get_device_id(self):
        return self.get_name().split("/")[2]

    def _identify_name_type(self):
        if "aggregate_model" in self.get_name():
            return ModelNameType.ROUND_AGGREGATE_MODEL
        elif "start_model" in self.get_name():
            return ModelNameType.ROUND_START_MODEL
        else:
            return ModelNameType.DEVICE_MODEL_UPDATE
