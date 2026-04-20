"""
Tests for /api/login and /api/register endpoints.
Covers: successful auth, invalid credentials, missing fields.
"""
import pytest


class TestLogin:
    """POST /api/login"""

    ENDPOINT = "/api/login"

    def test_valid_login_returns_200(self, api_client):
        payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        response = api_client.post(self.ENDPOINT, json=payload)
        assert response.status_code == 200

    def test_valid_login_returns_token(self, api_client):
        payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
        data = api_client.post(self.ENDPOINT, json=payload).json()
        assert "token" in data
        assert len(data["token"]) > 0

    def test_invalid_credentials_returns_400(self, api_client):
        payload = {"email": "wrong@email.com", "password": "badpass"}
        response = api_client.post(self.ENDPOINT, json=payload)
        assert response.status_code == 400

    def test_missing_password_returns_400(self, api_client):
        payload = {"email": "eve.holt@reqres.in"}
        response = api_client.post(self.ENDPOINT, json=payload)
        assert response.status_code == 400

    def test_missing_password_error_message(self, api_client):
        payload = {"email": "eve.holt@reqres.in"}
        data = api_client.post(self.ENDPOINT, json=payload).json()
        assert "error" in data
        assert "password" in data["error"].lower()

    def test_missing_email_returns_400(self, api_client):
        payload = {"password": "cityslicka"}
        response = api_client.post(self.ENDPOINT, json=payload)
        assert response.status_code == 400

    @pytest.mark.parametrize("email,password,expected_status", [
        ("eve.holt@reqres.in", "cityslicka", 200),
        ("invalid@email.com",  "badpass",    400),
        ("",                   "cityslicka", 400),
        ("eve.holt@reqres.in", "",           400),
    ])
    def test_login_parametrized(self, api_client, email, password, expected_status):
        payload = {k: v for k, v in {"email": email, "password": password}.items() if v}
        response = api_client.post(self.ENDPOINT, json=payload)
        assert response.status_code == expected_status


class TestRegister:
    """POST /api/register"""

    ENDPOINT = "/api/register"

    def test_valid_register_returns_200(self, api_client):
        payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
        response = api_client.post(self.ENDPOINT, json=payload)
        assert response.status_code == 200

    def test_valid_register_returns_id_and_token(self, api_client):
        payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
        data = api_client.post(self.ENDPOINT, json=payload).json()
        assert "id" in data
        assert "token" in data

    def test_missing_password_returns_400(self, api_client):
        payload = {"email": "eve.holt@reqres.in"}
        response = api_client.post(self.ENDPOINT, json=payload)
        assert response.status_code == 400

    def test_undefined_user_returns_400(self, api_client):
        payload = {"email": "nobody@domain.com", "password": "pass"}
        response = api_client.post(self.ENDPOINT, json=payload)
        assert response.status_code == 400

    def test_undefined_user_error_message(self, api_client):
        payload = {"email": "nobody@domain.com", "password": "pass"}
        data = api_client.post(self.ENDPOINT, json=payload).json()
        assert "error" in data
        assert len(data["error"]) > 0
