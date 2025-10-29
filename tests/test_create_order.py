import requests
import allure
import pytest
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data import CREATE_ORDER_URL, ORDER_DATA


@allure.suite('Создание заказа')
class TestCreateOrder:
    """Тесты для проверки создания заказа с разными цветами"""

    @allure.title('Проверка создания заказа с разными вариантами цветов')
    @allure.description('Можно создать заказ с цветом BLACK, GREY, обоими цветами или без цвета')
    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GREY'],
        []
    ])
    def test_create_order_with_different_colors_returns_track(self, color, created_order_track):
        """Проверка: можно создать заказ с разными вариантами цветов, тело ответа содержит track"""
        payload = ORDER_DATA.copy()
        payload["color"] = color

        response = requests.post(CREATE_ORDER_URL, json=payload)

        # Проверяем код ответа
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "track" in response_data, "В ответе нет поля 'track'"
        assert isinstance(response_data["track"], int), "Поле 'track' должно быть числом"
        
        # Сохраняем track для последующей отмены заказа
        created_order_track.append(response_data["track"])
