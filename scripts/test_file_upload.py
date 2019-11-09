import requests
import json

if __name__ == '__main__':
    data = {} # URL FROM AMAZON

    with open("model_1_2.model", 'rb') as f:
        response = requests.post(data["url"], data=data["fields"], files={"file" : (data["fields"]["key"], f)})
        print(response.status_code)
        print(response.reason)

    print("Done!")
