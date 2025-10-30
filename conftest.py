import pytest
import requests
from helpers import delete_courier, login_courier, generate_random_string
from data import CREATE_COURIER_URL, CANCEL_ORDER_URL


@pytest.fixture
def courier_data():
    """
    Фикстура для создания и удаления тестового курьера
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


@pytest.fixture
def courier_cleanup():
    """
    Фикстура для удаления курьера после теста
    Используется для тестов, где создание курьера - это шаг теста
    """
    couriers_to_delete = []
    
    yield couriers_to_delete
    
    # Удаляем всех курьеров после теста
    for courier_info in couriers_to_delete:
        courier_id = login_courier(courier_info["login"], courier_info["password"])
        if courier_id:
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
        requests.put(CANCEL_ORDER_URL, params={"track": track})
