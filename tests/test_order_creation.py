import allure
import pytest
from helpers import create_order, get_order_payload
from test_data import ORDER_COLORS

@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.title("Проверка статус-кода при создании заказа с цветом(ами): {color}")
    @pytest.mark.parametrize("color", ORDER_COLORS)
    def test_order_status_is_201(self, color):
        payload = get_order_payload(color)
        response = create_order(payload)
        assert response.status_code == 201, "Ожидается статус-код 201 при успешном создании заказа"

    @allure.title("Проверка наличия номера трека в ответе при цвете: {color}")
    @pytest.mark.parametrize("color", ORDER_COLORS)
    def test_order_response_contains_track(self, color):
        payload = get_order_payload(color)
        response = create_order(payload)
        assert "track" in response.json(), "Ответ должен содержать номер трека заказа"
