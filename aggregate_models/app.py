import json
import boto3
import os
from tempfile import NamedTemporaryFile

import torch
import torch.nn as nn
import torch.nn.functional as F

class FashionMNISTCNN(nn.Module):

    def __init__(self, num_outputs=10):
        super(FashionMNISTCNN, self).__init__()

        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2))

        self.fc = nn.Linear(7*7*32, num_outputs)

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)

        x = x.view(x.size(0), -1)

        x = self.fc(x)

        return x

def average_nn_parameters(parameters):
    """
    Averages passed parameters.

    :param parameters: nn model named parameters
    :type parameters: list
    """
    new_params = {}
    for name in parameters[0].keys():
        new_params[name] = sum([param[name].data for param in parameters]) / len(parameters)

    return new_params

def load_model_from_s3(object_name):
    BUCKET_NAME = os.environ["MODELS_BUCKET"]

    s3 = boto3.client('s3')
    model_file = NamedTemporaryFile(delete=True)

    parameters = {}
    try:
        with open(model_file.name, 'wb') as f:
            s3.download_fileobj(BUCKET_NAME, object_name, f)

            net = FashionMNISTCNN(num_outputs=10)
            net.load_state_dict(torch.load(model_file))

            parameters = dict(net.named_parameters())
    finally:
        model_file.close()

    return parameters

def generate_averaged_model(averaged_parameters):
    net = FashionMNISTCNN(num_outputs=10)
    with torch.no_grad():
        params = dict(net.named_parameters())
        for name in averaged_parameters.keys():
            params[name].set_(averaged_parameters[name])

    return net

def save_model_to_s3(object_name, model):
    BUCKET_NAME = os.environ["MODELS_BUCKET"]

    s3 = boto3.client('s3')
    model_file = NamedTemporaryFile(delete=True)
    try:
        with open(model_file.name, 'wb') as f:
            torch.save(model.state_dict(), f)

        with open(model_file.name, 'rb') as f:
            s3.upload_fileobj(f, BUCKET_NAME, object_name)
    finally:
        model_file.close()

def get_models_from_s3(round_id):
    """
    :param round_id: int
    """
    TABLE_NAME = os.environ["LEARNING_ROUND_TABLE_NAME"]

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)

    round_item = table.get_item(Key={"ID" : round_id})["Item"]

    model_parameters = []
    for model_update_info in round_item["model_updates"]:
        model_parameters.append(load_model_from_s3(model_update_info["model"]))

    return model_parameters

def lambda_handler(event, context):
    req_json = json.loads(event.get('body'))
    round_id = req_json["round_id"]

    # TODO : Authenticate user

    models = get_models_from_s3(round_id)
    averaged_parameters = average_nn_parameters(models)
    averaged_model = generate_averaged_model(averaged_parameters)
    save_model_to_s3(str(round_id), averaged_model)

    return {
        "statusCode" : 200,
        "body" : json.dumps({})
    }
