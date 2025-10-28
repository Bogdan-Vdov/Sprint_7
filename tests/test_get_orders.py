import requests
import allure
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data import GET_ORDERS_URL


@allure.suite('Получение списка заказов')
class TestGetOrders:
    """Тесты для проверки получения списка заказов"""

    @allure.title('Проверка получения списка заказов')
    @allure.description('В тело ответа возвращается список заказов')
    def test_get_orders_returns_list_of_orders(self):
        """Проверка: в тело ответа возвращается список заказов"""
        response = requests.get(GET_ORDERS_URL)

        # Проверяем код ответа
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "orders" in response_data, "В ответе нет поля 'orders'"
        assert isinstance(response_data["orders"], list), "Поле 'orders' должно быть списком"
