"""
Тесты для эндпоинта POST /api/Auth/signup.

API принимает только email/lang/utm
и отправляет на email ссылку для установки пароля.
"""
import pytest


class TestAuthSignup:
    """Тесты регистрации нового аккаунта."""

    SIGNUP_PATH = "/api/Auth/signup"

    """Позитивный тест."""
    def test_signup_success(self, api_session, new_user_payload):
        # Arrange
        url = f"{api_session.base_url}{self.SIGNUP_PATH}"
        
        # Act
        response = api_session.post(url, json=new_user_payload)

        # Assert
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["email"] == new_user_payload["email"]
        assert body["lang"] == "en"
        assert isinstance(body["token"], str) and body["token"]

    """Негативный: повторная регистрация того же email."""
    def test_signup_duplicate_email(self, api_session, new_user_payload):
        # Arrange
        url = f"{api_session.base_url}{self.SIGNUP_PATH}"
        first = api_session.post(url, json=new_user_payload)
        assert first.status_code == 200, first.text

        # Act — повторная регистрация с тем же email
        response = api_session.post(url, json=new_user_payload)

        # Assert
        assert response.status_code == 429, response.text
        body = response.json()
        assert body["error"]["code"] == "user.signup.resetTokenSent"
        assert body["error"]["values"]["email"] == new_user_payload["email"]

    """Негативный: пустое тело."""
    def test_signup_empty_body(self, api_session):
        # Arrange
        url = f"{api_session.base_url}{self.SIGNUP_PATH}"

        # Act
        response = api_session.post(url, json={})

        # Assert
        assert response.status_code == 409, response.text
        body = response.json()
        assert body["error"]["code"] == "user.email.notNull"

    """Негативный: невалидные email."""
    @pytest.mark.parametrize(
        "email,expected_code",
        [
            ("not-an-email", "user.email.isInvalid"),
            ("missing-at-sign.com", "user.email.isInvalid"),
            ("", "user.email.isRequired"),
        ],
    )
    def test_signup_invalid_email(
        self, api_session, new_user_payload, email, expected_code
    ):
        # Arrange
        url = f"{api_session.base_url}{self.SIGNUP_PATH}"
        payload = {**new_user_payload, "email": email}

        # Act
        response = api_session.post(url, json=payload)

        # Assert
        assert response.status_code == 409, response.text
        body = response.json()
        assert body["error"]["code"] == expected_code

    """Негативный: email отсутствует как ключ."""
    def test_signup_missing_email_field(self, api_session):
        # Arrange
        url = f"{api_session.base_url}{self.SIGNUP_PATH}"

        # Act — body без ключа email
        response = api_session.post(url, json={"lang": "en"})

        # Assert
        assert response.status_code == 409, response.text
        body = response.json()
        assert body["error"]["code"] == "user.email.notNull"