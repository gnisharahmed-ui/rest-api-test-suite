"""
Reusable API client wrapping requests.Session.
Provides centralized logging, error handling, and response validation.
"""
import logging
import time
import requests
from requests import Response

log = logging.getLogger(__name__)


class ApiClient:
    """
    Thin wrapper around requests.Session.
    Supports auth token injection, base URL composition, and request logging.
    """

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def set_auth_token(self, token: str):
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        log.info("Auth token set on session")

    def get(self, endpoint: str, **kwargs) -> Response:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response:
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Response:
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Response:
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        return self._request("DELETE", endpoint, **kwargs)

    def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        start = time.time()
        log.info("→ %s %s | body=%s", method, url, kwargs.get("json"))

        response = self.session.request(
            method, url, timeout=self.timeout, **kwargs
        )

        elapsed_ms = round((time.time() - start) * 1000)
        log.info("← %s %s | %dms | body=%s",
                 response.status_code, url, elapsed_ms,
                 response.text[:300] if response.text else "")
        return response
