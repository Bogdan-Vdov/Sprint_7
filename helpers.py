import requests
import random
import string
from data import CREATE_COURIER_URL, LOGIN_COURIER_URL, DELETE_COURIER_URL


def generate_random_string(length):
    """Генерирует случайную строку из букв нижнего регистра"""
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def register_new_courier_and_return_login_password():
    """
    Метод регистрации нового курьера возвращает список из логина, пароля и имени
    Если регистрация не удалась, возвращает пустой список
    """
    # Создаём список, чтобы метод мог его вернуть
    login_pass = []

    # Генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # Собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # Отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(CREATE_COURIER_URL, data=payload)

    # Если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # Возвращаем список
    return login_pass


def delete_courier(courier_id):
    """Удаляет курьера по ID"""
    if courier_id:
        response = requests.delete(f'{DELETE_COURIER_URL}/{courier_id}')
        return response


def login_courier(login, password):
    """Авторизует курьера и возвращает его ID"""
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(LOGIN_COURIER_URL, data=payload)
    if response.status_code == 200:
        return response.json().get("id")
    return None
