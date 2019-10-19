import json
import requests
from keras.models import Sequential
from keras.layers import Dense
import sys

def create_simple_model():
    model = Sequential()
    model.add(Dense(units=64, activation='relu', input_dim=100))
    model.add(Dense(units=10, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
        optimizer='sgd',
        metrics=['accuracy'])

    return model

def test_submit_model_update_function():
    model = create_simple_model()
    model_arch = model.to_json()
    model_params = list(model.get_weights())
    print(sys.getsizeof(model_params))
    payload = {"group_name" : "automated test group"}
    response = requests.request(url="http://127.0.0.1:3000/api/v1/create_group", method="post", json=payload)

    print(response.json())
