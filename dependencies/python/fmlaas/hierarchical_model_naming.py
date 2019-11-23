from .model_naming import ModelNameStructure

class HierarchicalModelNameStructure(ModelNameStructure):

    def _generate_model_object_name(self, group_id, round_id, device_id):
        return group_id + "/" + round_id + "/" + device_id

    def get_group_id(self):
        return int(self.get_name().split("/")[0])

    def get_round_id(self):
        return int(self.get_name().split("/")[1])

    def get_device_id(self):
        return int(self.get_name().split("/")[2])
