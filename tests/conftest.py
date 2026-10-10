import uuid

from faker import Faker
import pytest
import requests

# Константы
BASE_URL = "https://automation.tivaliclub.com/fcle"
fake = Faker()


@pytest.fixture(scope="session")
def api_base_url():
    """Возвращает базовый URL для тестируемого API.

    Использует scope='session', чтобы значение создавалось один раз за весь
    тестовый запуск.
    """
    return BASE_URL


@pytest.fixture(scope="class")
def api_session(api_base_url):
    """Создает и настраивает HTTP-сессию для выполнения запросов.

    Автоматически добавляет необходимые заголовки и закрывает сессию
    после завершения всех тестов в классе.
    """
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    session.base_url = api_base_url

    # Фаза ACT / YIELD: передаем управление тестам
    yield session

    # Фаза TEARDOWN: принудительно закрываем соединение после тестов
    session.close()


@pytest.fixture
def new_user_payload():
    """Генерирует уникальный JSON-тело (payload) для регистрации нового
    пользователя.

    Использует UUID для гарантированной уникальности email адреса.
    """
    unique = uuid.uuid4().hex[:12]
    return {
        "email": f"test_{unique}@example.com",
        "lang": "en",
        "utm": "",  # Обязательное поле для API, отправляется пустым
    }
