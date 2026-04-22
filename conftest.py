"""
Pytest configuration and shared fixtures for REST API test suite.
"""
import os
import pytest
import requests
from tests.utils.api_client import ApiClient
from tests.utils.auth_helper import AuthHelper


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="staging",
                     help="Environment: staging | production")
    parser.addoption("--base-url", action="store", default=None,
                     help="Override base URL")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def base_url(request, env):
    override = request.config.getoption("--base-url")
    if override:
        return override
    urls = {
        "staging":    "https://reqres.in",
        "production": "https://reqres.in",
    }
    return urls.get(env, urls["staging"])


@pytest.fixture(scope="session")
def api_client(base_url):
    """Session-scoped API client with base URL configured."""
    api_key = os.environ.get("REQRES_API_KEY")
    return ApiClient(base_url=base_url, api_key=api_key)


@pytest.fixture(scope="session")
def auth_token(api_client):
    """Obtain and cache auth token for the session."""
    return AuthHelper.get_token(api_client)


@pytest.fixture(scope="session")
def auth_client(api_client, auth_token):
    """API client pre-configured with auth token."""
    api_client.set_auth_token(auth_token)
    return api_client


@pytest.fixture(autouse=True)
def log_test_name(request):
    """Log test name before each test for easier debugging."""
    print(f"\n{'='*60}")
    print(f"TEST: {request.node.name}")
    print(f"{'='*60}")
