import requests
import allure
import pytest
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers import generate_random_string, login_courier, delete_courier
from data import CREATE_COURIER_URL


@allure.suite('Создание курьера')
class TestCreateCourier:
    """Тесты для проверки создания курьера"""

    @allure.title('Проверка успешного создания курьера')
    @allure.description('Курьера можно создать. Запрос возвращает код 201 и {"ok": true}')
    def test_create_courier_success_returns_201_and_ok_true(self, courier_cleanup):
        """Проверка: курьера можно создать, запрос возвращает код 201 и {'ok': true}"""
        # Генерируем данные для нового курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # Отправляем запрос на создание курьера
        response = requests.post(CREATE_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert response_data.get("ok") == True, f"Ожидалось {{'ok': true}}, получено {response_data}"

        # Добавляем курьера в список для удаления
        courier_cleanup.append({"login": login, "password": password})

    @allure.title('Проверка создания курьера с дублирующимся логином')
    @allure.description('Нельзя создать двух одинаковых курьеров')
    def test_create_courier_with_duplicate_login_returns_409_error(self, courier_cleanup):
        """Проверка: нельзя создать двух одинаковых курьеров"""
        # Создаём первого курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # Первый запрос - успешное создание
        first_response = requests.post(CREATE_COURIER_URL, data=payload)
        assert first_response.status_code == 201

        # Второй запрос с тем же логином - должен вернуть ошибку
        second_response = requests.post(CREATE_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert second_response.status_code == 409, f"Ожидался код 409, получен {second_response.status_code}"

        # Проверяем тело ответа
        response_data = second_response.json()
        assert "message" in response_data, "В ответе нет поля 'message'"

        # Добавляем курьера в список для удаления
        courier_cleanup.append({"login": login, "password": password})

    @allure.title('Проверка создания курьера без поля login')
    @allure.description('Если нет поля login, запрос возвращает ошибку')
    def test_create_courier_without_login_returns_400_error(self):
        """Проверка: если нет поля login, запрос возвращает ошибку"""
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "password": password,
            "firstName": first_name
        }

        response = requests.post(CREATE_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "message" in response_data, "В ответе нет поля 'message'"

    @allure.title('Проверка создания курьера без поля password')
    @allure.description('Если нет поля password, запрос возвращает ошибку')
    def test_create_courier_without_password_returns_400_error(self):
        """Проверка: если нет поля password, запрос возвращает ошибку"""
        login = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "firstName": first_name
        }

        response = requests.post(CREATE_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "message" in response_data, "В ответе нет поля 'message'"



    @allure.title('Проверка создания курьера с существующим логином')
    @allure.description('Если создать пользователя с логином, который уже есть, возвращается ошибка')
    def test_create_courier_with_existing_login_returns_409_error(self, courier_cleanup):
        """Проверка: если создать пользователя с логином, который уже есть, возвращается ошибка"""
        # Создаём первого курьера
        login = generate_random_string(10)
        password1 = generate_random_string(10)
        first_name1 = generate_random_string(10)

        payload1 = {
            "login": login,
            "password": password1,
            "firstName": first_name1
        }

        first_response = requests.post(CREATE_COURIER_URL, data=payload1)
        assert first_response.status_code == 201

        # Пытаемся создать второго курьера с тем же логином, но другими данными
        password2 = generate_random_string(10)
        first_name2 = generate_random_string(10)

        payload2 = {
            "login": login,
            "password": password2,
            "firstName": first_name2
        }

        second_response = requests.post(CREATE_COURIER_URL, data=payload2)

        # Проверяем код ответа
        assert second_response.status_code == 409, f"Ожидался код 409, получен {second_response.status_code}"

        # Проверяем тело ответа
        response_data = second_response.json()
        assert "message" in response_data, "В ответе нет поля 'message'"

        # Добавляем курьера в список для удаления
        courier_cleanup.append({"login": login, "password": password1})
