import pytest
import requests
from helpers import delete_courier, login_courier, generate_random_string
from data import CREATE_COURIER_URL, CANCEL_ORDER_URL


@pytest.fixture
def new_courier():
    """
    Фикстура для создания и удаления курьера
    Возвращает словарь с данными курьера
    """
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
    requests.post(CREATE_COURIER_URL, data=payload)
    
    courier_info = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    # Возвращаем данные курьера для использования в тесте
    yield courier_info
    
    # Удаляем курьера после теста (teardown)
    courier_id = login_courier(login, password)
    delete_courier(courier_id)


@pytest.fixture
def created_order_track():
    """
    Фикстура для отмены созданного заказа
    Сохраняет track заказа и отменяет его после теста
    """
    track_numbers = []
    
    yield track_numbers
    
    # Отменяем все созданные заказы
    for track in track_numbers:
        requests.put(CANCEL_ORDER_URL, json={"track": track})
