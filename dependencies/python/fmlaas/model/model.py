from ..hierarchical_model_naming import HierarchicalModelNameStructure

class Model:

    def __init__(self, entity_id, name, size):
        """
        :param entity_id: string. ID of the entity that produced this model
        :param name: dict
        :param size: string. Size of model in bytes
        """
        self.entity_id = entity_id
        self.name = name
        self.size = size

    def set_entity_id(self, entity_id):
        self.entity_id = entity_id

    def get_entity_id(self):
        return self.entity_id

    def get_name(self):
        # TODO : Maybe serialize the model name type as well so this isn't hardcoded?
        #   Another option: Merge name logic into Model since it is an attribute
        return HierarchicalModelNameStructure().load_name(self.name)

    def get_size(self):
        return self.size

    def to_json(self):
        return {
            "entity_id" : self.entity_id,
            "name" : self.name,
            "size" : self.size
        }

    @staticmethod
    def from_json(json_data):
        return Model(json_data["entity_id"], json_data["name"], json_data["size"])

    @staticmethod
    def is_valid_json(json_data):
        return "entity_id" in json_data and "name" in json_data and "size" in json_data
