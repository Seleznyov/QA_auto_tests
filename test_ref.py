import json
import random
import string

import requests
import pytest
from settings import root_url, headers


url = f"{root_url}/users"
users = []

def test_get_users():
    response = requests.get(url)
    body_type = type(response.json())
    expected_body_type = list

    assert body_type == expected_body_type
    for i in response.json():
        users.append(i.get("username"))


def test_create_user():
    rand_name = ''.join(random.choices(string.ascii_letters, k=3))
    rand_pass = ''.join(random.choices(string.ascii_letters, k=3))
    data = {"username": "Test_" + rand_name, "email": "test@test.com", "password": "Test_" + rand_pass}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    assert response.status_code == 201
    user_id = response.json().get("id")

    user_url = f"{url}/{user_id}"
    response = requests.get(user_url)
    assert response.status_code == 200

    response_data = response.json()
    del response_data["id"]
    assert response_data == data


def test_update_user():
    rand_name = ''.join(random.choices(string.ascii_letters, k=3))
    rand_pass = ''.join(random.choices(string.ascii_letters, k=3))
    data = {"username": "Test_" + rand_name, "email": "test@test.com", "password": "Test_" + rand_pass}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        rand_name_new = ''.join(random.choices(string.ascii_letters, k=4))
        new_user_id = response.json().get("id")
        test_get_users()
        new_name = "test_update_user01"
        if new_name in users:
            new_name = new_name+rand_name_new
            upd_user_payload = {"username": new_name}
            response = requests.put(f"{url}/{new_user_id}", headers=headers, data=json.dumps(upd_user_payload))
            assert response.status_code == 201

            user_url = f"{url}/{new_user_id}"
            get_user_response = requests.get(user_url)
            assert get_user_response.json().get("username") == new_name

        if new_name not in users:
            upd_user_payload = {"username": new_name}
            response = requests.put(f"{url}/{new_user_id}", headers=headers, data=json.dumps(upd_user_payload))
            assert response.status_code == 201


