"""
Tests for /api/users endpoint.
Covers: GET list, GET single, POST, PUT, PATCH, DELETE + schema validation.
"""
import pytest
from tests.utils.schema_validator import assert_response, assert_schema


class TestGetUsers:
    """GET /api/users — list users"""

    def test_get_users_returns_200(self, api_client):
        response = api_client.get("/api/users", params={"page": 1})
        assert_response(response, 200, "users_list_schema.json")

    def test_get_users_default_page_is_1(self, api_client):
        response = api_client.get("/api/users").json()
        assert response["page"] == 1

    def test_get_users_page_2(self, api_client):
        response = api_client.get("/api/users", params={"page": 2})
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 2
        assert len(data["data"]) > 0

    def test_get_users_returns_correct_per_page(self, api_client):
        response = api_client.get("/api/users", params={"per_page": 3})
        data = response.json()
        assert len(data["data"]) <= 3

    def test_get_users_pagination_metadata_present(self, api_client):
        data = api_client.get("/api/users").json()
        assert all(k in data for k in ["page", "per_page", "total", "total_pages"])

    def test_get_users_total_pages_calculated_correctly(self, api_client):
        data = api_client.get("/api/users").json()
        import math
        expected_pages = math.ceil(data["total"] / data["per_page"])
        assert data["total_pages"] == expected_pages


class TestGetSingleUser:
    """GET /api/users/{id} — single user"""

    def test_get_user_by_id_returns_200(self, api_client):
        response = api_client.get("/api/users/2")
        assert_response(response, 200, "user_schema.json")

    def test_get_user_by_id_returns_correct_id(self, api_client):
        data = api_client.get("/api/users/2").json()
        assert data["data"]["id"] == 2

    def test_get_user_email_format(self, api_client):
        data = api_client.get("/api/users/2").json()
        email = data["data"]["email"]
        assert "@" in email and "." in email

    def test_get_nonexistent_user_returns_404(self, api_client):
        response = api_client.get("/api/users/9999")
        assert response.status_code == 404

    def test_get_nonexistent_user_returns_empty_body(self, api_client):
        response = api_client.get("/api/users/9999")
        assert response.json() == {}


class TestCreateUser:
    """POST /api/users — create user"""

    def test_create_user_returns_201(self, api_client):
        payload = {"name": "Jane Doe", "job": "SDET Lead"}
        response = api_client.post("/api/users", json=payload)
        assert_response(response, 201, "create_user_schema.json")

    def test_create_user_response_matches_payload(self, api_client):
        payload = {"name": "Ahmed", "job": "Senior SDET"}
        data = api_client.post("/api/users", json=payload).json()
        assert data["name"] == payload["name"]
        assert data["job"] == payload["job"]

    def test_create_user_generates_id(self, api_client):
        payload = {"name": "Test User", "job": "QA"}
        data = api_client.post("/api/users", json=payload).json()
        assert "id" in data and data["id"]

    def test_create_user_generates_timestamp(self, api_client):
        payload = {"name": "Test User", "job": "QA"}
        data = api_client.post("/api/users", json=payload).json()
        assert "createdAt" in data and data["createdAt"]

    @pytest.mark.parametrize("name,job", [
        ("Alice", "Engineer"),
        ("Bob", "Manager"),
        ("Carol", "Designer"),
    ])
    def test_create_user_parametrized(self, api_client, name, job):
        payload = {"name": name, "job": job}
        response = api_client.post("/api/users", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == name


class TestUpdateUser:
    """PUT and PATCH /api/users/{id} — update user"""

    def test_put_user_returns_200(self, api_client):
        payload = {"name": "Updated Name", "job": "Updated Job"}
        response = api_client.put("/api/users/2", json=payload)
        assert response.status_code == 200

    def test_put_user_response_has_updated_at(self, api_client):
        payload = {"name": "Updated", "job": "SDET"}
        data = api_client.put("/api/users/2", json=payload).json()
        assert "updatedAt" in data

    def test_patch_user_returns_200(self, api_client):
        payload = {"job": "Lead SDET"}
        response = api_client.patch("/api/users/2", json=payload)
        assert response.status_code == 200

    def test_patch_user_partial_update(self, api_client):
        payload = {"job": "Principal SDET"}
        data = api_client.patch("/api/users/2", json=payload).json()
        assert data["job"] == payload["job"]


class TestDeleteUser:
    """DELETE /api/users/{id}"""

    def test_delete_user_returns_204(self, api_client):
        response = api_client.delete("/api/users/2")
        assert response.status_code == 204

    def test_delete_user_returns_empty_body(self, api_client):
        response = api_client.delete("/api/users/2")
        assert response.text == ""


class TestChainedUserFlow:
    """
    Chained API test: Create → Get → Update → Delete
    Demonstrates end-to-end API workflow testing.
    """

    def test_full_user_lifecycle(self, api_client):
        # Step 1: Create
        create_payload = {"name": "Lifecycle User", "job": "QA Engineer"}
        create_resp = api_client.post("/api/users", json=create_payload)
        assert create_resp.status_code == 201
        user_id = create_resp.json()["id"]
        assert user_id, "Created user should have an ID"

        # Step 2: Verify exists (reqres.in doesn't persist, so we just verify structure)
        assert_schema(create_resp.json(), "create_user_schema.json")

        # Step 3: Update
        update_payload = {"name": "Updated Lifecycle User", "job": "Senior QA"}
        update_resp = api_client.put(f"/api/users/{user_id}", json=update_payload)
        assert update_resp.status_code == 200
        assert update_resp.json()["name"] == "Updated Lifecycle User"

        # Step 4: Delete
        delete_resp = api_client.delete(f"/api/users/{user_id}")
        assert delete_resp.status_code == 204
