import pytest
import allure
from helpers import register_courier, login_courier, delete_courier, generate_random_string


@pytest.fixture
@allure.step("Регистрация и удаление курьера после теста")
def registered_courier(request, generate_courier_data):
    register_response = register_courier(generate_courier_data)
    assert register_response.status_code == 201, "Курьер должен быть успешно зарегистрирован"

    login_response = login_courier(generate_courier_data)
    assert login_response.status_code == 200, "Логин должен быть успешным"
    courier_id = login_response.json()["id"]

    def tear_down():
        delete_courier(courier_id)

    request.addfinalizer(tear_down)

    return generate_courier_data, register_response, login_response

@pytest.fixture
@allure.step('Генерация данных для создания курьера')
def generate_courier_data():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }

