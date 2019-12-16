from .model_naming import ModelNameStructure
from .model_name_type import ModelNameType

class HierarchicalModelNameStructure(ModelNameStructure):

    def _generate_model_object_name(self, group_id, round_id, device_id):
        return group_id + "/" + round_id + "/" + device_id

    def get_group_id(self):
        return int(self.get_name().split("/")[0])

    def get_round_id(self):
        return int(self.get_name().split("/")[1])

    def get_device_id(self):
        return int(self.get_name().split("/")[2])

    def _identify_name_type(self):
        if len(self.get_name().split("/")) == 2:
            if self.get_group_id() == self.get_round_id():
                return ModelNameType.INITIAL_GROUP_MODEL
        elif self.get_device_id() == self.get_round_id():
            return ModelNameType.ROUND_AGGREGATE_MODEL
        else:
            return ModelNameType.DEVICE_MODEL_UPDATE

        raise ValueError("Could not parse model name to identify type: {}".format(self.get_name()))
