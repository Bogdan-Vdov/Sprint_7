import pytest
import requests
from helpers import delete_courier, login_courier


@pytest.fixture
def courier_data():
    """
    Фикстура для создания и удаления тестового курьера
    Возвращает словарь с данными курьера
    """
    from helpers import generate_random_string, CREATE_COURIER_URL
    
    # Создаём данные курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    # Создаём курьера
    response = requests.post(CREATE_COURIER_URL, data=payload)
    
    courier_info = {
        "login": login,
        "password": password,
        "firstName": first_name,
        "id": None
    }
    
    # Возвращаем данные курьера для использования в тесте
    yield courier_info
    
    # Удаляем курьера после теста (teardown)
    if courier_info["id"] is None:
        courier_id = login_courier(login, password)
        if courier_id:
            delete_courier(courier_id)
    else:
        delete_courier(courier_info["id"])
