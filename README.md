# 🔌 REST API Test Suite

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-8.1-green?logo=pytest)
![jsonschema](https://img.shields.io/badge/Schema_Validation-jsonschema-orange)
![CI](https://github.com/gnisharahmed-ui/rest-api-test-suite/actions/workflows/api-tests.yml/badge.svg)

A senior-level REST API test suite built with Python and Pytest — featuring schema validation, auth token management, chained API flows, parallel execution, and HTML reporting.

---

## 📐 Architecture

```
rest-api-test-suite/
├── tests/
│   ├── api/
│   │   ├── test_users.py      # CRUD + chained lifecycle tests
│   │   └── test_auth.py       # Login / register tests
│   ├── schemas/
│   │   ├── user_schema.json
│   │   ├── users_list_schema.json
│   │   └── create_user_schema.json
│   └── utils/
│       ├── api_client.py      # Requests wrapper with logging
│       ├── auth_helper.py     # Token retrieval
│       └── schema_validator.py
├── postman/                   # Exported Postman collection + environment
├── conftest.py                # Session fixtures: api_client, auth_token
├── pytest.ini
├── requirements.txt
└── .github/workflows/
```

## 🔑 Key Design Decisions

| Concern | Solution |
|---|---|
| HTTP Client | `requests.Session` wrapped in `ApiClient` for centralized logging |
| Auth | Token obtained once per session via `AuthHelper`, injected into all requests |
| Schema Validation | `jsonschema` against versioned JSON schema files |
| Parallelism | `pytest-xdist` with `-n auto` for parallel test execution |
| Reporting | `pytest-html` self-contained HTML report |
| Environments | `--env` CLI flag with URL mapping; `--base-url` override |

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run against specific environment
pytest --env=staging

# Run only auth tests
pytest tests/api/test_auth.py -v

# Run with parallel workers
pytest -n 4

# Generate HTML report
pytest --html=reports/report.html --self-contained-html
```

---

## ✅ Test Coverage

| Module | Tests |
|---|---|
| `test_users.py` | GET list, pagination, GET by ID, 404, POST, PUT, PATCH, DELETE, chained lifecycle |
| `test_auth.py` | Valid login, invalid creds, missing fields, register, parametrized auth matrix |

**Test against:** [reqres.in](https://reqres.in) — a free, public REST API for testing.

---

## 📋 Schema Validation Example

```python
def test_get_user_by_id_returns_200(self, api_client):
    response = api_client.get("/api/users/2")
    assert_response(response, 200, "user_schema.json")
```

Schemas live in `tests/schemas/` as versioned JSON Schema Draft-07 files.

---

## 🏗️ CI/CD

GitHub Actions runs tests on Python 3.11 and 3.12 in parallel on every push and PR.
HTML reports are uploaded as artifacts.

See [`.github/workflows/api-tests.yml`](.github/workflows/api-tests.yml)
