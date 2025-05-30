BASE_URL = "https://qa-scooter.praktikum-services.ru"

#Ручки согласно: https://qa-scooter.praktikum-services.ru/docs/
COURIER_ENDPOINT = "/api/v1/courier"
COURIER_LOGIN_ENDPOINT = "/api/v1/courier/login"
ORDER_ENDPOINT = "/api/v1/orders"
ORDERS_LIST_ENDPOINT = "/api/v1/orders"

#Данные для параметризации
COURIER_DATA = ["login", "password", "firstName"]
LOGIN_DATA = ["login", "password"]
ORDER_COLORS = [["BLACK"], ["GREY"], ["BLACK", "GREY"], []]

# Шаблон заказа из документации
ORDER_DEFAULT_BODY = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha",
    "color": []
}