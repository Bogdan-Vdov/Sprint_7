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
