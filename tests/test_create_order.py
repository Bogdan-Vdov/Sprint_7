import requests
import allure
import pytest
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data import CREATE_ORDER_URL


@allure.suite('Создание заказа')
class TestCreateOrder:
    """Тесты для проверки создания заказа с разными цветами"""

    @allure.title('Проверка создания заказа с цветом BLACK')
    @allure.description('Можно указать один из цветов — BLACK')
    @pytest.mark.parametrize('color', [['BLACK']])
    def test_create_order_with_black_color_returns_track(self, color):
        """Проверка: можно указать цвет BLACK, тело ответа содержит track"""
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-12-06",
            "comment": "Test order",
            "color": color
        }

        response = requests.post(CREATE_ORDER_URL, json=payload)

        # Проверяем код ответа
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "track" in response_data, "В ответе нет поля 'track'"
        assert isinstance(response_data["track"], int), "Поле 'track' должно быть числом"

    @allure.title('Проверка создания заказа с цветом GREY')
    @allure.description('Можно указать один из цветов — GREY')
    @pytest.mark.parametrize('color', [['GREY']])
    def test_create_order_with_grey_color_returns_track(self, color):
        """Проверка: можно указать цвет GREY, тело ответа содержит track"""
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-12-06",
            "comment": "Test order",
            "color": color
        }

        response = requests.post(CREATE_ORDER_URL, json=payload)

        # Проверяем код ответа
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "track" in response_data, "В ответе нет поля 'track'"
        assert isinstance(response_data["track"], int), "Поле 'track' должно быть числом"

    @allure.title('Проверка создания заказа с обоими цветами')
    @allure.description('Можно указать оба цвета — BLACK и GREY')
    @pytest.mark.parametrize('color', [['BLACK', 'GREY']])
    def test_create_order_with_both_colors_returns_track(self, color):
        """Проверка: можно указать оба цвета, тело ответа содержит track"""
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-12-06",
            "comment": "Test order",
            "color": color
        }

        response = requests.post(CREATE_ORDER_URL, json=payload)

        # Проверяем код ответа
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "track" in response_data, "В ответе нет поля 'track'"
        assert isinstance(response_data["track"], int), "Поле 'track' должно быть числом"

    @allure.title('Проверка создания заказа без цвета')
    @allure.description('Можно совсем не указывать цвет')
    @pytest.mark.parametrize('color', [[]])
    def test_create_order_without_color_returns_track(self, color):
        """Проверка: можно не указывать цвет, тело ответа содержит track"""
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-12-06",
            "comment": "Test order",
            "color": color
        }

        response = requests.post(CREATE_ORDER_URL, json=payload)

        # Проверяем код ответа
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "track" in response_data, "В ответе нет поля 'track'"
        assert isinstance(response_data["track"], int), "Поле 'track' должно быть числом"
