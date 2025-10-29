"""
Базовый URL и эндпоинты для API Яндекс.Самокат
"""

BASE_URL = 'https://qa-scooter.praktikum-services.ru'

# Эндпоинты для курьеров
CREATE_COURIER_URL = f'{BASE_URL}/api/v1/courier'
LOGIN_COURIER_URL = f'{BASE_URL}/api/v1/courier/login'
DELETE_COURIER_URL = f'{BASE_URL}/api/v1/courier'

# Эндпоинты для заказов
CREATE_ORDER_URL = f'{BASE_URL}/api/v1/orders'
GET_ORDERS_URL = f'{BASE_URL}/api/v1/orders'
CANCEL_ORDER_URL = f'{BASE_URL}/api/v1/orders/cancel'

# Данные для создания заказа
ORDER_DATA = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2024-12-06",
    "comment": "Test order"
}

# Тексты ошибок
ERROR_MESSAGES = {
    "insufficient_data_for_creation": "Недостаточно данных для создания учетной записи",
    "duplicate_login": "Этот логин уже используется. Попробуйте другой.",
    "insufficient_data_for_login": "Недостаточно данных для входа",
    "account_not_found": "Учетная запись не найдена"
}
