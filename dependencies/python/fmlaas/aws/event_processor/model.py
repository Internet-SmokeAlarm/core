from .event_processor import EventProcessor
from ...model import Model
from ...hierarchical_model_naming import HierarchicalModelNameStructure

class ModelUploadEventProcessor(EventProcessor):

    def process_event(self, json_data):
        models_uploaded = []

        for record in json_data["Records"]:
            object = record["s3"]["object"]
            object_key = object["key"]
            object_size = object["size"]

            object_name = HierarchicalModelNameStructure()
            object_name.load_name(object_key)

            model = Model(None, object_name.get_name(), str(object_size))

            models_uploaded.append(model)

        return models_uploaded
