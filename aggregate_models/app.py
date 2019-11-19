import json
from tempfile import NamedTemporaryFile

from fmlaas import download_s3_object
from fmlaas import upload_s3_object
from fmlaas_pytorch import combine_models
from fmlaas_pytorch import scale_model
from fmlaas_pytorch.serde import deserialize_state_dict
from fmlaas_pytorch.serde import serialize_numpy
from fmlaas_pytorch.storage import DiskModelStorage
from fmlaas import get_group_table_name_from_env
from fmlaas import DynamoDBInterface
from fmlaas import FLGroup

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
            global_model = combine_models(global_model, new_model)

    return global_model

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    group_id = req_json["group_id"]
    round_id = req_json["round_id"]

    # TODO : Authenticate user

    dynamodb_ = DynamoDBInterface(get_group_table_name_from_env())
    group = FLGroup.load_from_db(group_id, dynamodb_)

    models = group.get_models(round_id)
    num_models = len(models)

    global_model = generate_global_model(models)
    scaled_global_model = scale_model(global_model, num_models)

    save_model_to_s3(str(round_id), scaled_global_model)
    group.set_round_global_model(round_id, str(round_id))

    FLGroup.save_to_db(group, dynamodb_)

    return {
        "statusCode" : 200,
        "body" : json.dumps({})
    }
