import allure
import json
import requests
import random
import string
from test_data import *

@allure.step('Генерация строки из {length} символов')
def generate_random_string(length = 10):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

@allure.step('Генерация данных для создания курьера')
def generate_courier_data():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }

@allure.step('Отправка запроса на ручку POST: /api/v1/courier с данными: {courier_data}')
def register_courier(courier_data):
    response = requests.post(f"{BASE_URL}{COURIER_ENDPOINT}", data=courier_data)
    return response

@allure.step('Отправка запроса на ручку POST: /api/v1/courier/login с данными: {courier_data}')
def login_courier(courier_data):
    response = requests.post(f"{BASE_URL}{COURIER_LOGIN_ENDPOINT}", data=courier_data)
    return response

@allure.step('Отправка запроса на ручку DELETE: /api/v1/courier/{courier_id} для удаления курьера после тестов')
def delete_courier(courier_id):
    delete_response = requests.delete(f"{BASE_URL}{COURIER_ENDPOINT}/{courier_id}")
    assert delete_response.status_code == 200, f"Курьер {courier_id} должен быть удален"

@allure.step('Очистка созданного курьера после теста')
def clear_courier(response):
    courier_id = response.json()["id"]
    delete_response = requests.delete(f"{BASE_URL}{COURIER_ENDPOINT}/{courier_id}")
    assert delete_response.status_code == 200, f"Курьер {courier_id} должен быть удален"

@allure.step('Отправка запроса на ручку PUT: /api/v1/orders/finish/:id')
def create_order(order_data):
    response = requests.post(f"{BASE_URL}{ORDER_ENDPOINT}", json=order_data)
    return response

@allure.step('Отправка запроса на ручку GET: /api/v1/orders')
def get_orders_list():
    response = requests.get(f"{BASE_URL}{ORDERS_LIST_ENDPOINT}")
    return response

@allure.step('Генерация данных для заказа с цветом(ами): {color}')
def get_order_payload(color=None):
    payload = ORDER_DEFAULT_BODY.copy()
    payload["color"] = color if color else []
    return payload