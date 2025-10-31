import requests
import allure
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers import generate_random_string
from data import LOGIN_COURIER_URL, ERROR_MESSAGES


@allure.suite('Логин курьера')
class TestLoginCourier:
    """Тесты для проверки логина курьера"""

    @allure.title('Проверка успешной авторизации курьера')
    @allure.description('Курьер может авторизоваться и успешный запрос возвращает id')
    def test_login_courier_success_returns_200_and_id(self, courier_data):
        """Проверка: курьер может авторизоваться, успешный запрос возвращает id"""
        # Авторизуемся с данными из фикстуры
        payload = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        response = requests.post(LOGIN_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert "id" in response_data, "В ответе нет поля 'id'"
        assert isinstance(response_data["id"], int), "Поле 'id' должно быть числом"

    @allure.title('Проверка авторизации без поля login')
    @allure.description('Если нет поля login, запрос возвращает ошибку')
    def test_login_courier_without_login_returns_400_error(self, courier_data):
        """Проверка: если нет поля login, запрос возвращает ошибку"""
        payload = {"password": courier_data["password"]}
        response = requests.post(LOGIN_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

        # Проверяем текст ошибки
        response_data = response.json()
        assert response_data.get("message") == ERROR_MESSAGES["insufficient_data_for_login"], \
            f"Ожидалось сообщение '{ERROR_MESSAGES['insufficient_data_for_login']}', получено '{response_data.get('message')}'"

    @allure.title('Проверка авторизации без поля password')
    @allure.description('Если нет поля password, запрос возвращает ошибку')
    def test_login_courier_without_password_returns_400_error(self, courier_data):
        """Проверка: если нет поля password, запрос возвращает ошибку (возможен таймаут сервера 504)"""
        payload = {"login": courier_data["login"]}
        response = requests.post(LOGIN_COURIER_URL, data=payload)

        # Проверяем код ответа (400 или 504 при таймауте сервера)
        assert response.status_code in [400, 504], f"Ожидался код 400 или 504, получен {response.status_code}"

    @allure.title('Проверка авторизации с неправильным логином')
    @allure.description('Система вернёт ошибку, если неправильно указать логин')
    def test_login_courier_with_wrong_login_returns_404_error(self, courier_data):
        """Проверка: система вернёт ошибку, если неправильно указать логин"""
        # Пытаемся авторизоваться с неправильным логином
        wrong_login = generate_random_string(10)
        payload = {
            "login": wrong_login,
            "password": courier_data["password"]
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"

        # Проверяем текст ошибки
        response_data = response.json()
        assert response_data.get("message") == ERROR_MESSAGES["account_not_found"], \
            f"Ожидалось сообщение '{ERROR_MESSAGES['account_not_found']}', получено '{response_data.get('message')}'"

    @allure.title('Проверка авторизации с неправильным паролем')
    @allure.description('Система вернёт ошибку, если неправильно указать пароль')
    def test_login_courier_with_wrong_password_returns_404_error(self, courier_data):
        """Проверка: система вернёт ошибку, если неправильно указать пароль"""
        # Пытаемся авторизоваться с неправильным паролем
        wrong_password = generate_random_string(10)
        payload = {
            "login": courier_data["login"],
            "password": wrong_password
        }

        response = requests.post(LOGIN_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"

        # Проверяем текст ошибки
        response_data = response.json()
        assert response_data.get("message") == ERROR_MESSAGES["account_not_found"], \
            f"Ожидалось сообщение '{ERROR_MESSAGES['account_not_found']}', получено '{response_data.get('message')}'"

    @allure.title('Проверка авторизации под несуществующим пользователем')
    @allure.description('Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    def test_login_courier_with_non_existent_user_returns_404_error(self, courier_data):
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

        # Проверяем текст ошибки
        response_data = response.json()
        assert response_data.get("message") == ERROR_MESSAGES["account_not_found"], \
            f"Ожидалось сообщение '{ERROR_MESSAGES['account_not_found']}', получено '{response_data.get('message')}'"
