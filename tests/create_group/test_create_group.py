import requests

def test_create_group_function():
    payload = {"group_name" : "automated_test_group"}
    response = requests.request(url="http://127.0.0.1:3000/api/v1/create_group", method="post", json=payload)

    print(response.json())
