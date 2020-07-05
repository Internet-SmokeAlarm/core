from .event_processor import EventProcessor
from ...model import Model
from ...s3_storage import PointerFactory


class ModelUploadEventProcessor(EventProcessor):

    def process_event(self, json_data):
        models_uploaded = []

        for record in json_data["Records"]:
            object = record["s3"]["object"]
            object_key = object["key"]
            object_size = object["size"]

            s3_pointer = PointerFactory.load_pointer(object_key)
            model = Model(None, str(s3_pointer), str(object_size))

            models_uploaded.append(model)

        return models_uploaded
