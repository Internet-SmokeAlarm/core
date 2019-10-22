import requests
import json
import requests
from keras.models import Sequential
from keras.layers import Dense

def create_simple_model():
    model = Sequential()
    model.add(Dense(units=64, activation='relu', input_dim=100))
    model.add(Dense(units=10, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
        optimizer='sgd',
        metrics=['accuracy'])

    return model

if __name__ == '__main__':
    data = {} # URL FROM AMAZON

    model = create_simple_model()
    model_arch = model.to_json()

    #model.load_weights("/Users/valetolpegin/Downloads/group_key_111_100ace_0")
    #model.save_weights("test_weights.h5")
    #print("LOADED")
    #exit(0)

    with open("test_weights.h5", 'rb') as f:
        response = requests.post(data["url"], data=data["fields"], files={"file" : (data["fields"]["key"], f)})
        print(response.status_code)
        print(response.reason)

    print("Done!")
