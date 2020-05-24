from tempfile import NamedTemporaryFile
import json

from fmlaas.aws import download_s3_object
from fmlaas.aws import upload_s3_object
from fmlaas.aggregation import FederatedAveraging
from fmlaas.serde import deserialize_state_dict
from fmlaas.serde import serialize_numpy
from fmlaas.storage import DiskModelStorage
from fmlaas import get_job_table_name_from_env
from fmlaas.database import DynamoDBInterface
from fmlaas.model import DBObject
from fmlaas.model import Job
from fmlaas.model import Model
from fmlaas.request_processor import IDProcessor
from fmlaas import HierarchicalModelNameStructure


def load_model_from_s3(object_name):
    model_file = NamedTemporaryFile(delete=True)

    state_dict = None
    try:
        with open(model_file.name, 'wb') as f:
            download_s3_object(object_name, f)

        with open(model_file.name, 'r') as f:
            deserialized_model = DiskModelStorage.load_model(f)
            state_dict = deserialize_state_dict(deserialized_model)
    finally:
        model_file.close()

    return state_dict


def save_model_to_s3(object_name, model):
    model_file = NamedTemporaryFile(delete=True)
    try:
        with open(model_file.name, 'w') as f:
            serializeable_state_dict = serialize_numpy(model)
            DiskModelStorage.store_model(f, serializeable_state_dict)

        with open(model_file.name, 'rb') as f:
            upload_s3_object(object_name, f)
    finally:
        model_file.close()


def generate_global_model(models):
    """
    :param models: list(torch.nn)
    """
    global_model = None

    for model in models:
        if global_model is None:
            global_model = load_model_from_s3(model)
        else:
            new_model = load_model_from_s3(model)
            global_model = FederatedAveraging().combine_models(global_model, new_model)

    return global_model


def lambda_handler(event, context):
    try:
        id_processor = IDProcessor(event)
        job_id = id_processor.get_job_id()
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": str(error)
        }

    dynamodb_ = DynamoDBInterface(get_job_table_name_from_env())
    job = DBObject.load_from_db(Job, job_id, dynamodb_)

    name = HierarchicalModelNameStructure()
    name.generate_name(job_id=job_id)

    models = job.get_models()
    model_names = [models[model].get_name().get_name()
                   for model in models.keys()]
    num_models = len(model_names)

    global_model = generate_global_model(model_names)
    scaled_global_model = FederatedAveraging().scale_model(global_model, num_models)

    save_model_to_s3(name.get_name(), scaled_global_model)

    return {
        "statusCode": 200,
        "body": "{}"
    }
