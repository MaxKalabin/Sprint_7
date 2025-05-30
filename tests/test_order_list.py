import allure
from helpers import get_orders_list

@allure.feature("Список заказов")
class TestOrderList:

    @allure.title("Получение списка всех заказов")
    def test_get_answer_has_list(self):
        response = get_orders_list()
        assert response.status_code == 200, "Ожидается статус-код 200 при успешном получении списка заказов"

        data = response.json()
        assert "orders" in data, "Ответ должен содержать ключ 'orders'"
        assert isinstance(data["orders"], list), "Поле 'orders' должно быть списком"

        for order in data["orders"]:
            assert isinstance(order, dict), "Каждый заказ должен быть объектом (dict)"