import requests
import allure
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers import generate_random_string
from data import CREATE_COURIER_URL, ERROR_MESSAGES


@allure.suite('Создание курьера')
class TestCreateCourier:
    """Тесты для проверки создания курьера"""

    @allure.title('Проверка успешного создания курьера')
    @allure.description('Курьера можно создать. Запрос возвращает код 201 и {"ok": true}')
    def test_create_courier_success_returns_201_and_ok_true(self, new_courier):
        """Проверка: курьера можно создать, запрос возвращает код 201 и {'ok': true}"""
        # Используем данные из фикстуры для создания нового курьера
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

    @allure.title('Проверка создания курьера с дублирующимся логином')
    @allure.description('Нельзя создать двух одинаковых курьеров')
    def test_create_courier_with_duplicate_login_returns_409_error(self, new_courier):
        """Проверка: нельзя создать двух одинаковых курьеров"""
        # Используем данные уже созданного курьера из фикстуры
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"],
            "firstName": new_courier["firstName"]
        }

        # Пытаемся создать второго курьера с теми же данными
        response = requests.post(CREATE_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 409, f"Ожидался код 409, получен {response.status_code}"

        # Проверяем текст ошибки
        response_data = response.json()
        assert response_data.get("message") == ERROR_MESSAGES["duplicate_login"], \
            f"Ожидалось сообщение '{ERROR_MESSAGES['duplicate_login']}', получено '{response_data.get('message')}'"

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

        # Проверяем текст ошибки
        response_data = response.json()
        assert response_data.get("message") == ERROR_MESSAGES["insufficient_data_for_creation"], \
            f"Ожидалось сообщение '{ERROR_MESSAGES['insufficient_data_for_creation']}', получено '{response_data.get('message')}'"

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

        # Проверяем текст ошибки
        response_data = response.json()
        assert response_data.get("message") == ERROR_MESSAGES["insufficient_data_for_creation"], \
            f"Ожидалось сообщение '{ERROR_MESSAGES['insufficient_data_for_creation']}', получено '{response_data.get('message')}'"

    @allure.title('Проверка создания курьера с существующим логином')
    @allure.description('Если создать пользователя с логином, который уже есть, возвращается ошибка')
    def test_create_courier_with_existing_login_returns_409_error(self, new_courier):
        """Проверка: если создать пользователя с логином, который уже есть, возвращается ошибка"""
        # Пытаемся создать курьера с логином, который уже существует (из фикстуры)
        payload = {
            "login": new_courier["login"],
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response = requests.post(CREATE_COURIER_URL, data=payload)

        # Проверяем код ответа
        assert response.status_code == 409, f"Ожидался код 409, получен {response.status_code}"

        # Проверяем текст ошибки
        response_data = response.json()
        assert response_data.get("message") == ERROR_MESSAGES["duplicate_login"], \
            f"Ожидалось сообщение '{ERROR_MESSAGES['duplicate_login']}', получено '{response_data.get('message')}'"
