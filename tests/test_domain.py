import pytest

def test_fr_001_register_returns_jwt(client):
    email = "unique_user@example.com"
    password = "securepassword123"
    response = client.post("/api/auth/register", json={"email": email, "password": password})
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_fr_002_login_returns_jwt(client):
    email = "unique_user_login@example.com"
    password = "securepassword123"
    client.post("/api/auth/register", json={"email": email, "password": password})
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_fr_003_create_todo(client, auth_headers):
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "due_date": "2023-12-31"
    }
    response = client.post("/api/todos", json=todo_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["title"] == todo_data["title"]
    assert response.json()["description"] == todo_data["description"]
    assert response.json()["due_date"] == todo_data["due_date"]

def test_fr_004_get_todos(client, auth_headers):
    todo_data = {
        "title": "Unique Todo for FR-004",
        "description": "Test description",
        "due_date": "2023-12-31"
    }
    client.post("/api/todos", json=todo_data, headers=auth_headers)
    response = client.get("/api/todos", headers=auth_headers)
    assert response.status_code == 200
    assert any(todo["title"] == todo_data["title"] for todo in response.json())

def test_fr_005_get_completed_todos(client, auth_headers):
    todo_data = {
        "title": "Completed Todo",
        "description": "Test description",
        "due_date": "2023-12-31",
        "completed": True
    }
    client.post("/api/todos", json=todo_data, headers=auth_headers)
    response = client.get("/api/todos?completed=true", headers=auth_headers)
    assert response.status_code == 200
    assert all(todo["completed"] for todo in response.json())
    assert any(todo["title"] == todo_data["title"] for todo in response.json())

def test_fr_006_get_todo_by_id(client, auth_headers):
    todo_data = {
        "title": "Todo for FR-006",
        "description": "Test description",
        "due_date": "2023-12-31"
    }
    create_response = client.post("/api/todos", json=todo_data, headers=auth_headers)
    todo_id = create_response.json()["id"]
    response = client.get(f"/api/todos/{todo_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == todo_data["title"]
    assert response.json()["description"] == todo_data["description"]

def test_fr_007_update_todo(client, auth_headers):
    todo_data = {
        "title": "Todo for FR-007",
        "description": "Initial description",
        "due_date": "2023-12-31"
    }
    create_response = client.post("/api/todos", json=todo_data, headers=auth_headers)
    todo_id = create_response.json()["id"]
    updated_data = {
        "title": "Updated Title",
        "description": "Updated description",
        "due_date": "2024-01-01",
        "completed": True
    }
    update_response = client.put(f"/api/todos/{todo_id}", json=updated_data, headers=auth_headers)
    assert update_response.status_code == 200
    assert update_response.json()["title"] == updated_data["title"]
    assert update_response.json()["description"] == updated_data["description"]
    assert update_response.json()["due_date"] == updated_data["due_date"]
    assert update_response.json()["completed"] == updated_data["completed"]

def test_fr_008_patch_todo_completed(client, auth_headers):
    todo_data = {
        "title": "Todo for FR-008",
        "description": "Test description",
        "due_date": "2023-12-31",
        "completed": False
    }
    create_response = client.post("/api/todos", json=todo_data, headers=auth_headers)
    todo_id = create_response.json()["id"]
    patch_response = client.patch(f"/api/todos/{todo_id}", json={"completed": True}, headers=auth_headers)
    assert patch_response.status_code == 200
    assert patch_response.json()["completed"] is True

def test_fr_009_delete_todo(client, auth_headers):
    todo_data = {
        "title": "Todo for FR-009",
        "description": "Test description",
        "due_date": "2023-12-31"
    }
    create_response = client.post("/api/todos", json=todo_data, headers=auth_headers)
    todo_id = create_response.json()["id"]
    delete_response = client.delete(f"/api/todos/{todo_id}", headers=auth_headers)
    assert delete_response.status_code == 200
    assert delete_response.json() == {"status": "deleted"}
    get_response = client.get(f"/api/todos/{todo_id}", headers=auth_headers)
    assert get_response.status_code == 404