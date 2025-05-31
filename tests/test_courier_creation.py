import allure
import pytest

from helpers import register_courier
from test_data import COURIER_DATA, OK_TRUE_ANSWER, LOGIN_EXIST_ERROR, INSUFFICIENT_DATA_FOR_REGISTRATION_ERROR

@allure.feature("Создание курьера")
class TestCourierCreation:

    @allure.title("Проверка статус-кода при создании курьера с уникальными данными")
    def test_create_courier_status_is_201(self, registered_courier):
        _, response, _ = registered_courier
        assert response.status_code == 201, "Курьер должен быть создан"

    @allure.title("Проверка текста ответа при создании курьера с уникальными данными")
    def test_create_courier_response_ok_true(self, registered_courier):
        _, response, _ = registered_courier
        assert OK_TRUE_ANSWER in response.text, 'Ответ при успешном создании курьера должен быть {"ok":true}'

    @allure.title("Проверка статус-кода при создании курьера с существующим логином")
    def test_create_courier_duplicate_login_status_is_409(self, registered_courier):
        сourier_data, _, _ = registered_courier
        second_response = register_courier(сourier_data)
        assert second_response.status_code == 409, "Ожидается статус-код 409 при дублировании логина"

    @allure.title("Проверка сообщения об ошибке при создании курьера с существующим логином")
    def test_create_courier_duplicate_login_error_message_duplicate_login(self, registered_courier):
        courier_data, _, _ = registered_courier
        second_response = register_courier(courier_data)
        assert LOGIN_EXIST_ERROR in second_response.text, "Ошибка не содержит ожидаемое сообщение"

    @allure.title("Проверка статус-кода при отсутствии обязательного поля")
    @pytest.mark.parametrize("missing_field", COURIER_DATA)
    def test_create_courier_missing_required_fields_status_is_400(self, missing_field, generate_courier_data):
        del generate_courier_data[missing_field]
        response = register_courier(generate_courier_data)
        assert response.status_code == 400

    @allure.title("Проверка сообщения об ошибке при отсутствии обязательного поля")
    @pytest.mark.parametrize("missing_field", COURIER_DATA)
    def test_create_courier_missing_required_fields_error_message_insufficient_data(self, missing_field, generate_courier_data):
        del generate_courier_data[missing_field]
        response = register_courier(generate_courier_data)
        assert INSUFFICIENT_DATA_FOR_REGISTRATION_ERROR in response.text