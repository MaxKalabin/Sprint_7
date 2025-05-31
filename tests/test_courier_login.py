import allure
import pytest
from test_data import TEXT_ID, LOGIN_DATA, INSUFFICIENT_DATA_FOR_LOGIN_ERROR, ACCOUNT_NOT_FOUND_ERROR
from helpers import login_courier

@allure.feature("Логин курьера")
class TestCourierLogin:
    @allure.title("Проверка статус-кода, при авторизация курьера с валидными данными")
    def test_login_courier_status_is_200(self, registered_courier):
        payload, _, login_response = registered_courier
        assert login_response.status_code == 200, "Ожидается статус-код 200 при успешной авторизации"

    @allure.title("Проверка наличия в ответе id авторизованного курьера, при авторизация курьера с валидными данными")
    def test_login_courier_response_has_courier_id(self, registered_courier):
        payload, _, _ = registered_courier
        login_response = login_courier(payload)
        assert TEXT_ID in login_response.json(), "Ответ должен содержать ID курьера"

    @allure.title("Проверка статус-кода, при передаче во время логина данных без поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", LOGIN_DATA)
    def test_login_courier_missing_required_fields_status_is_400(self, missing_field, registered_courier):
        valid_payload, _, _ = registered_courier

        invalid_payload = valid_payload.copy()
        del invalid_payload[missing_field]
        login_response = login_courier(invalid_payload)
        assert login_response.status_code == 400, f"Ожидается статус-код 400 при отсутствии поля {missing_field}"

    @allure.title("Проверка текста ошибки, при передаче во время логина данных без поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", LOGIN_DATA)
    def test_login_courier_missing_required_fields_error_message_insufficient_data(self, missing_field, registered_courier):
        valid_payload, _, _ = registered_courier

        invalid_payload = valid_payload.copy()
        del invalid_payload[missing_field]
        login_response = login_courier(invalid_payload)
        assert INSUFFICIENT_DATA_FOR_LOGIN_ERROR in login_response.text, "Ошибка не содержит ожидаемое сообщение"

    @allure.title("Проверка статус-кода, при авторизации с неверной парой логин-пароль, с ошибкой в поле: {wrong_field}")
    @pytest.mark.parametrize("wrong_field", LOGIN_DATA)
    def test_login_courier_invalid_credentials_status_is_404(self, wrong_field, registered_courier):
        valid_payload, _, _ = registered_courier

        invalid_payload = valid_payload.copy()
        invalid_payload[wrong_field] = "wrong_" + invalid_payload[wrong_field]
        login_response = login_courier(invalid_payload)
        assert login_response.status_code == 404, f"Ожидается статус-код 404 при неверном {wrong_field}"

    @allure.title("Проверка текста ошибки, при авторизации с неверной парой логин-пароль, с ошибкой в поле: {wrong_field}")
    @pytest.mark.parametrize("wrong_field", LOGIN_DATA)
    def test_login_courier_invalid_credentials_error_message_not_found(self, wrong_field, registered_courier):
        valid_payload, _, _ = registered_courier

        invalid_payload = valid_payload.copy()
        invalid_payload[wrong_field] = "wrong_" + invalid_payload[wrong_field]
        login_response = login_courier(invalid_payload)
        assert ACCOUNT_NOT_FOUND_ERROR in login_response.text, "Ошибка не содержит ожидаемое сообщение"

    @allure.title("Проверка статус-кода, при авторизации несуществующего курьера")
    def test_login_nonexistent_courier_status_is_404(self, generate_courier_data):
        response = login_courier(generate_courier_data)
        assert response.status_code == 404, "Ожидается статус-код 404 для несуществующего курьера"

    @allure.title("Проверка текста ошибки, при авторизации несуществующего курьера")
    def test_login_nonexistent_courier_error_message_not_found(self, generate_courier_data):
        response = login_courier(generate_courier_data)
        assert ACCOUNT_NOT_FOUND_ERROR in response.text, "Ошибка не содержит ожидаемое сообщение"
