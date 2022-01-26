import json
import random
import string

import requests
from settings import root_url, headers

import pytest


#GET
def test_get_posts():
    url = f"{root_url}/posts"
    response = requests.get(url)
    if response.json() == []:
        print("Нет постов, вызвать запрос на создание")
        test_create_posts()
    assert response.status_code == 200
    return response.json()[-1]

#POST
def test_create_posts():
    url = f"{root_url}/posts"
    rand_title = ''.join(random.choices(string.ascii_letters, k=3))
    rand_text = ''.join(random.choices(string.ascii_letters, k=3))
    rand_uthor_id = random.randint(1,100)
    data = {"title": "title_"+rand_title,"text": "text_"+rand_text, "author_id": rand_uthor_id}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    assert response.status_code == 201

    last_title = response.json().get("title")
    assert last_title == test_get_posts().get("title")
    last_author_id = response.json().get("author_id")
    assert type(last_author_id) == int


#GET
def test_get_users():
    url = f"{root_url}/users"
    response = requests.get(url)
    body_type = type(response.json())
    expected_body_type = list
    assert body_type == expected_body_type
    return response.json()[-1].get("id")

#POST
def test_create_user():
    url = f"{root_url}/users"
    rand_name = ''.join(random.choices(string.ascii_letters, k=3))
    rand_pass = ''.join(random.choices(string.ascii_letters, k=3))
    data = {"username": "Test_"+rand_name,"email": "test@test.com","password": "Test_"+rand_pass}

    id_before = test_get_users()
    response = requests.post(url, headers=headers, data=json.dumps(data))
    id_after = test_get_users()

    assert id_before + 1 == id_after
    assert response.status_code == 201