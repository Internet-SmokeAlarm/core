from .model_naming import ModelNameStructure
from .model_name_type import ModelNameType

class HierarchicalModelNameStructure(ModelNameStructure):

    def _generate_model_object_name(self, group_id=None, round_id=None, device_id=None):
        """
        :param group_id: string
        :param round_id: string
        :param device_id: string
        """
        if round_id == None and device_id == None:
            return self._generate_initial_group_model_name(group_id)
        elif device_id == None:
            return self._generate_aggregate_round_model_name(group_id, round_id)
        else:
            return self._generate_device_model_update_name(group_id, round_id, device_id)

    def _generate_device_model_update_name(self, group_id, round_id, device_id):
        """
        :param group_id: string
        :param round_id: string
        :param device_id: string
        """
        return group_id + "/" + round_id + "/" + device_id

    def _generate_initial_group_model_name(self, group_id):
        """
        :param group_id: string
        """
        return group_id + "/" + group_id

    def _generate_aggregate_round_model_name(self, group_id, round_id):
        """
        :param group_id: string
        :param ronud_id: string
        """
        return group_id + "/" + round_id + "/" + round_id

    def get_group_id(self):
        return self.get_name().split("/")[0]

    def get_round_id(self):
        return self.get_name().split("/")[1]

    def get_device_id(self):
        return self.get_name().split("/")[2]

    def _identify_name_type(self):
        if len(self.get_name().split("/")) == 2:
            if self.get_group_id() == self.get_round_id():
                return ModelNameType.INITIAL_GROUP_MODEL
        elif self.get_device_id() == self.get_round_id():
            return ModelNameType.ROUND_AGGREGATE_MODEL
        else:
            return ModelNameType.DEVICE_MODEL_UPDATE

        raise ValueError("Could not parse model name to identify type: {}".format(self.get_name()))
