import allure
import pytest
from test_data import COURIER_DATA
from helpers import generate_courier_data, register_courier, clear_courier, login_courier

@allure.feature("Создание курьера")
class TestCourierCreation:

    @allure.title("Проверка статус-кода при создании курьера с уникальными данными")
    def test_create_courier_status_is_201(self):
        payload = generate_courier_data()
        response = register_courier(payload)
        assert response.status_code == 201, "Курьер должен быть создан"
        clear_courier(login_courier(payload))

    @allure.title("Проверка текста ответа при создании курьера с уникальными данными")
    def test_create_courier_response_ok_true(self):
        payload = generate_courier_data()
        response = register_courier(payload)
        assert '{"ok":true}' in response.text, 'Ответ при успешном создании курьера должен быть {"ok":true}'
        if response.status_code == 201:
            clear_courier(login_courier(payload))

    @allure.title("Проверка статус-кода при создании курьера с существующим логином")
    def test_create_courier_duplicate_login_status_is_409(self):
        payload = generate_courier_data()
        register_courier(payload)
        second_response = register_courier(payload)
        assert second_response.status_code == 409, "Ожидается статус-код 409 при дублировании логина"

    @allure.title("Проверка сообщения об ошибке при создании курьера с существующим логином")
    def test_create_courier_duplicate_login_error_message_duplicate_login(self):
        payload = generate_courier_data()
        response = register_courier(payload)
        second_response = register_courier(payload)
        assert "Этот логин уже используется" in second_response.text, "Ошибка не содержит ожидаемое сообщение"
        if response.status_code == 201:
            clear_courier(login_courier(payload))

    @allure.title("Проверка статус-кода при отсутствии обязательного поля")
    @pytest.mark.parametrize("missing_field", COURIER_DATA)
    def test_create_courier_missing_required_fields_status_is_400(self, missing_field):
        payload = generate_courier_data()
        del payload[missing_field]
        response = register_courier(payload)
        assert response.status_code == 400

    @allure.title("Проверка сообщения об ошибке при отсутствии обязательного поля")
    @pytest.mark.parametrize("missing_field", COURIER_DATA)
    def test_create_courier_missing_required_fields_error_message_insufficient_data(self, missing_field):
        payload = generate_courier_data()
        del payload[missing_field]
        response = register_courier(payload)
        assert "Недостаточно данных для создания учетной записи" in response.text
        if response.status_code == 201:
            clear_courier(login_courier(payload))