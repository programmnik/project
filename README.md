# Test Automation Project — Auth Signup API

Автоматизированные тесты для эндпоинта `POST /api/Auth/signup` API
[automation.tivaliclub.com](https://automation.tivaliclub.com/fcle/swagger/index.html).

## Описание

Эндпоинт `/api/Auth/signup` — это **первый шаг регистрации**: API принимает
`email`, `lang` и `utm`, валидирует email и отправляет на него письмо со
ссылкой для установки пароля (см. `/api/Auth/set-password`). Пароль и
username в этом эндпоинте **не передаются**.

Тесты проверяют:
- успешную регистрацию нового пользователя;
- повторную регистрацию того же email (429, `user.signup.resetTokenSent`);
- пустое тело запроса (409, `user.email.notNull`);
- отсутствие поля `email` в теле (409, `user.email.notNull`);
- невалидные форматы email (409, `user.email.isInvalid` / `user.email.isRequired`).

## Установка

```bash
pip install -r requirements.txt
```

Рекомендуется использовать виртуальное окружение:

```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Запуск тестов

```bash
python -m pytest tests/ -v
```

или с использованием `pytest.ini` через команду 

```bash
python -m pytest
```

## Структура проекта

```
project/
│
├── tests/
│   ├── __init__.py          # маркер пакета
│   ├── conftest.py          # фикстуры: api_session, api_base_url, new_user_payload
│   └── test_signup.py       # тесты для /api/Auth/signup
├── requirements.txt         # зависимости
├── README.md                # этот файл
└── .gitignore               # игнорируемые файлы
```

## Пример ожидаемого вывода

```
============================= test session starts =============================
collected 7 items

tests/test_signup.py::TestAuthSignup::test_signup_success PASSED          [ 14%]
tests/test_signup.py::TestAuthSignup::test_signup_duplicate_email PASSED  [ 28%]
tests/test_signup.py::TestAuthSignup::test_signup_empty_body PASSED       [ 42%]
tests/test_signup.py::TestAuthSignup::test_signup_invalid_email[not-an-email-user.email.isInvalid] PASSED  [ 57%]
tests/test_signup.py::TestAuthSignup::test_signup_invalid_email[missing-at-sign.com-user.email.isInvalid] PASSED  [ 71%]
tests/test_signup.py::TestAuthSignup::test_signup_invalid_email[-user.email.isRequired] PASSED  [ 85%]
tests/test_signup.py::TestAuthSignup::test_signup_missing_email_field PASSED  [100%]

============================== 7 passed in 1.12s ==============================
```

## Особенности реализации

- **Фикстура `api_session`** (`scope="class"`) — единая `requests.Session` с
  установленным `Content-Type: application/json` и атрибутом `base_url`;
  закрывается автоматически после класса тестов.
- **`api_base_url`** (`scope="session"`) — базовый URL задаётся в одном месте.
- **`new_user_payload`** — генерирует уникальный email через `uuid4().hex`
  для каждого теста, что обеспечивает идемпотентность при повторных запусках.
- **Параметризация** `@pytest.mark.parametrize` — проверка нескольких
  невалидных email-адресов в одном тесте.
- **Паттерн AAA** (Arrange–Act–Assert) — каждая секция явно выделена
  комментариями в тестах.