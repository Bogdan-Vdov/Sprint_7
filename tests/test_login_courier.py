import requests
import allure
import pytest
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers import (generate_random_string, register_new_courier_and_return_login_password, 
                     login_courier, delete_courier)
from data import CREATE_COURIER_URL, LOGIN_COURIER_URL


@allure.suite('Логин курьера')
class TestLoginCourier:
    """Тесты для проверки логина курьера"""

    @allure.title('Проверка успешной авторизации курьера')
    @allure.description('Курьер может авторизоваться и успешный запрос возвращает id')
    def test_login_courier_success_returns_200_and_id(self):
        """Проверка: курьер может авторизоваться, успешный запрос возвращает id"""
        # Создаём нового курьера
        courier_data = register_new_courier_and_return_login_password()
        login = courier_data[0]
        password = courier_data[1]

        # Авторизуемся
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(LOGIN_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "id" in response_data, "В ответе нет поля 'id'"
        assert isinstance(response_data["id"], int), "Поле 'id' должно быть числом"

        # Удаляем курьера
        courier_id = response_data["id"]
        delete_courier(courier_id)

    @allure.title('Проверка авторизации без поля login')
    @allure.description('Если нет поля login, запрос возвращает ошибку')
    def test_login_courier_without_login_returns_400_error(self):
        """Проверка: если какого-то поля нет (login), запрос возвращает ошибку"""
        password = generate_random_string(10)

        payload = {
            "password": password
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "message" in response_data, "В ответе нет поля 'message'"

    @allure.title('Проверка авторизации без поля password')
    @allure.description('Если нет поля password, запрос возвращает ошибку')
    def test_login_courier_without_password_returns_400_error(self):
        """Проверка: если какого-то поля нет (password), запрос возвращает ошибку"""
        login = generate_random_string(10)

        payload = {
            "login": login
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "message" in response_data, "В ответе нет поля 'message'"

    @allure.title('Проверка авторизации с неправильным логином')
    @allure.description('Система вернёт ошибку, если неправильно указать логин')
    def test_login_courier_with_wrong_login_returns_404_error(self):
        """Проверка: система вернёт ошибку, если неправильно указать логин"""
        # Создаём курьера
        courier_data = register_new_courier_and_return_login_password()
        login = courier_data[0]
        password = courier_data[1]

        # Пытаемся авторизоваться с неправильным логином
        wrong_login = generate_random_string(10)
        payload = {
            "login": wrong_login,
            "password": password
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "message" in response_data, "В ответе нет поля 'message'"

        # Удаляем курьера
        courier_id = login_courier(login, password)
        delete_courier(courier_id)

    @allure.title('Проверка авторизации с неправильным паролем')
    @allure.description('Система вернёт ошибку, если неправильно указать пароль')
    def test_login_courier_with_wrong_password_returns_404_error(self):
        """Проверка: система вернёт ошибку, если неправильно указать пароль"""
        # Создаём курьера
        courier_data = register_new_courier_and_return_login_password()
        login = courier_data[0]
        password = courier_data[1]

        # Пытаемся авторизоваться с неправильным паролем
        wrong_password = generate_random_string(10)
        payload = {
            "login": login,
            "password": wrong_password
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "message" in response_data, "В ответе нет поля 'message'"

        # Удаляем курьера
        courier_id = login_courier(login, password)
        delete_courier(courier_id)

    @allure.title('Проверка авторизации под несуществующим пользователем')
    @allure.description('Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    def test_login_courier_with_non_existent_user_returns_404_error(self):
        """Проверка: если авторизоваться под несуществующим пользователем, запрос возвращает ошибку"""
        # Генерируем данные несуществующего пользователя
        login = generate_random_string(10)
        password = generate_random_string(10)

        payload = {
            "login": login,
            "password": password
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "message" in response_data, "В ответе нет поля 'message'"
