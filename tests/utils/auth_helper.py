"""
Auth helper for obtaining and caching JWT/Bearer tokens.
"""
import logging

log = logging.getLogger(__name__)


class AuthHelper:
    """
    Handles token retrieval for authenticated API tests.
    Uses reqres.in's /api/login endpoint for demo purposes.
    """

    LOGIN_ENDPOINT = "/api/login"

    @staticmethod
    def get_token(api_client) -> str:
        payload = {
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
        response = api_client.post(AuthHelper.LOGIN_ENDPOINT, json=payload)

        assert response.status_code == 200, \
            f"Login failed: {response.status_code} | {response.text}"

        token = response.json().get("token")
        assert token, "Token not found in login response"
        log.info("Auth token obtained successfully")
        return token
