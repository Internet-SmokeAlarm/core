import requests

def test_create_group_function():
    payload = {"group_name" : "automated test group"}
    #response = requests.request(url="http://127.0.0.1:3000/api/v1/create_group", method="post", json=payload)
    response = requests.request(url="https://lnifk4x538.execute-api.us-east-1.amazonaws.com/Prod/api/v1/create_group", method="post", json=payload)

    print(response.json())
