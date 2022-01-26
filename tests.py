import requests
import json

import random
import string
from settings import root_url,headers

#GET
def test_get_users():
	url = f"{root_url}/users"
	response = requests.get(url)
	body_type = type(response.json())
	expected_body_type = list
	if body_type == expected_body_type:
		print(f"Тест test_get_users PASSED. Expected data type is {expected_body_type}")
	else:
		print(f"Тест test_get_users FAILED. Expected data type: {expected_body_type}. Actual data type: {body_type}")
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

	if id_before + 1 == id_after:
		print("Тест test_create_user №1 PASSED добавлен новый пользователь")
	else:
		print(f"Тест test_create_user №1 FAILED, {id_before} + 1 == {id_after}")

	if response.status_code == 201:
		print(f"Тест test_create_user №2  PASSED. User with data {data} was created successfully")
	else:
		print(f"Тест test_create_user №2  FAILED. Status code: {response.status_code}. Error: {response.json()}")

#GET
def test_get_posts():
	url = f"{root_url}/posts"
	response = requests.get(url)
	if response.json() == []:
		print("Нет постов, вызвать запрос на создание")
		test_create_posts()
	if response.status_code == 200:
		print(f"Тест test_get_posts №1  PASSED, {response.status_code}")
	else:
		print(f"Тест test_get_posts №1  FAILED, {response.status_code}. Error: {response.json()}")
	return response.json()[-1]

#POST
def test_create_posts():
	url = f"{root_url}/posts"
	rand_title = ''.join(random.choices(string.ascii_letters, k=3))
	rand_text = ''.join(random.choices(string.ascii_letters, k=3))
	rand_uthor_id = random.randint(1,100)
	data = {"title": "title_"+rand_title,"text": "text_"+rand_text, "author_id": rand_uthor_id}

	response = requests.post(url, headers=headers, data=json.dumps(data))

	if response.status_code == 201:
		print(f"Тест  test_create_posts №1  PASSED, {response.status_code}")
	else:
		print(f"Тест test_create_posts №1  FAILED, {response.status_code}. Error: {response.json()}")

	last_title = response.json().get("title")
	if last_title == test_get_posts().get("title"):
		print(f"Тест  test_create_posts №2  PASSED")
	else:
		print(f"Тест  test_create_posts №3  FAILED, {last_title} == title"+{rand_title})
	last_author_id = response.json().get("author_id")
	if type(last_author_id) == int:
		print("Тест  test_create_posts №3  PASSED, тип значения last_author_id == int")
	else:
		print(f"Тест  test_create_posts №3  FAILED, тип значения last_author_id == {type(last_author_id)}, ожидалось int")