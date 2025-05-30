import allure
import pytest
from test_data import LOGIN_DATA
from helpers import generate_courier_data, login_courier, register_courier, clear_courier


@allure.feature("Логин курьера")
class TestCourierLogin:
    @allure.title("Проверка статус-кода, при авторизация курьера с валидными данными")
    def test_login_courier_status_is_200(self):
        payload = generate_courier_data()
        register_response = register_courier(payload)
        assert register_response.status_code == 201, "Ожидается статус-код 201 при успешной регистрации"

        login_response = login_courier(payload)
        assert login_response.status_code == 200, "Ожидается статус-код 200 при успешной авторизации"
        clear_courier(login_response)

    @allure.title("Проверка наличия в ответе id авторизованного курьера, при авторизация курьера с валидными данными")
    def test_login_courier_response_has_courier_id(self):
        payload = generate_courier_data()
        register_response = register_courier(payload)
        assert register_response.status_code == 201, "Ожидается статус-код 201 при успешной регистрации"

        login_response = login_courier(payload)
        assert "id" in login_response.json(), "Ответ должен содержать ID курьера"
        clear_courier(login_response)

    @allure.title("Проверка статус-кода, при передаче во время логина данных без поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", LOGIN_DATA)
    def test_login_courier_missing_required_fields_status_is_400(self, missing_field):
        valid_payload = generate_courier_data()
        register_response = register_courier(valid_payload)
        assert register_response.status_code == 201, "Ожидается статус-код 201 при успешной регистрации"

        invalid_payload = valid_payload.copy()
        del invalid_payload[missing_field]
        login_response = login_courier(invalid_payload)
        assert login_response.status_code == 400, f"Ожидается статус-код 400 при отсутствии поля {missing_field}"
        clear_courier(login_courier(valid_payload))

    @allure.title("Проверка текста ошибки, при передаче во время логина данных без поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", LOGIN_DATA)
    def test_login_courier_missing_required_fields_error_message_insufficient_data(self, missing_field):
        valid_payload = generate_courier_data()
        register_response = register_courier(valid_payload)
        assert register_response.status_code == 201, "Ожидается статус-код 201 при успешной регистрации"

        invalid_payload = valid_payload.copy()
        del invalid_payload[missing_field]
        login_response = login_courier(invalid_payload)
        assert "Недостаточно данных для входа" in login_response.text, "Ошибка не содержит ожидаемое сообщение"
        clear_courier(login_courier(valid_payload))

    @allure.title("Проверка статус-кода, при авторизации с неверной парой логин-пароль, с ошибкой в поле: {wrong_field}")
    @pytest.mark.parametrize("wrong_field", LOGIN_DATA)
    def test_login_courier_invalid_credentials_status_is_404(self, wrong_field):
        valid_payload = generate_courier_data()
        register_response = register_courier(valid_payload)
        assert register_response.status_code == 201, "Ожидается статус-код 201 при успешной регистрации"

        invalid_payload = valid_payload.copy()
        invalid_payload[wrong_field] = "wrong_" + invalid_payload[wrong_field]
        login_response = login_courier(invalid_payload)
        assert login_response.status_code == 404, f"Ожидается статус-код 404 при неверном {wrong_field}"
        clear_courier(login_courier(valid_payload))

    @allure.title("Проверка текста ошибки, при авторизации с неверной парой логин-пароль, с ошибкой в поле: {wrong_field}")
    @pytest.mark.parametrize("wrong_field", LOGIN_DATA)
    def test_login_courier_invalid_credentials_error_message_not_found(self, wrong_field):
        valid_payload = generate_courier_data()
        register_response = register_courier(valid_payload)
        assert register_response.status_code == 201, "Ожидается статус-код 201 при успешной регистрации"

        invalid_payload = valid_payload.copy()
        invalid_payload[wrong_field] = "wrong_" + invalid_payload[wrong_field]
        login_response = login_courier(invalid_payload)
        assert "Учетная запись не найдена" in login_response.text, "Ошибка не содержит ожидаемое сообщение"
        clear_courier(login_courier(valid_payload))

    @allure.title("Проверка статус-кода, при авторизации несуществующего курьера")
    def test_login_nonexistent_courier_status_is_404(self):
        payload = generate_courier_data()
        response = login_courier(payload)
        assert response.status_code == 404, "Ожидается статус-код 404 для несуществующего курьера"

    @allure.title("Проверка текста ошибки, при авторизации несуществующего курьера")
    def test_login_nonexistent_courier_error_message_not_found(self):
        payload = generate_courier_data()
        response = login_courier(payload)
        assert "Учетная запись не найдена" in response.text, "Ошибка не содержит ожидаемое сообщение"