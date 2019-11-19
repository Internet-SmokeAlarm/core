import requests
import json

MODEL_FILE_PATH = "tests/fmlaas_pytorch/data/mnist_cnn.json"

if __name__ == '__main__':
    data = {} # URL FROM AMAZON

    with open(MODEL_FILE_PATH, 'rb') as f:
        response = requests.post(data["url"], data=data["fields"], files={"file" : (data["fields"]["key"], f)})
        print(response.status_code)
        print(response.reason)

    print("Done!")
