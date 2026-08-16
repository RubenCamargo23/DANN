def _create_user(client, username="jdoe", email="jdoe@example.com"):
    return client.post(
        "/users",
        json={
            "username": username,
            "password": "secret123",
            "email": email,
            "dni": "123456",
            "fullName": "John Doe",
            "phoneNumber": "3000000000",
        },
    )


def test_ping(client):
    response = client.get("/users/ping")
    assert response.status_code == 200
    assert response.text == "pong"


def test_create_user_success(client):
    response = _create_user(client)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert "createdAt" in body


def test_create_user_duplicate(client):
    _create_user(client)
    response = _create_user(client)
    assert response.status_code == 412


def test_update_user_success(client):
    created = _create_user(client).json()
    response = client.patch(f"/users/{created['id']}", json={"fullName": "Jane Doe"})
    assert response.status_code == 200


def test_update_user_not_found(client):
    response = client.patch("/users/does-not-exist", json={"fullName": "Jane Doe"})
    assert response.status_code == 404


def test_update_user_no_fields(client):
    created = _create_user(client).json()
    response = client.patch(f"/users/{created['id']}", json={})
    assert response.status_code == 400


def test_update_user_invalid_status(client):
    created = _create_user(client).json()
    response = client.patch(f"/users/{created['id']}", json={"status": "INVALID"})
    assert response.status_code == 400


def test_auth_success(client):
    _create_user(client)
    response = client.post(
        "/users/auth", json={"username": "jdoe", "password": "secret123"}
    )
    assert response.status_code == 200
    assert "token" in response.json()


def test_auth_invalid_credentials(client):
    _create_user(client)
    response = client.post(
        "/users/auth", json={"username": "jdoe", "password": "wrong"}
    )
    assert response.status_code == 404


def test_get_me_success(client):
    _create_user(client)
    auth = client.post(
        "/users/auth", json={"username": "jdoe", "password": "secret123"}
    ).json()
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {auth['token']}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "jdoe"


def test_get_me_missing_header(client):
    response = client.get("/users/me")
    assert response.status_code == 403


def test_get_me_invalid_token(client):
    response = client.get(
        "/users/me", headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401


def test_count_users(client):
    _create_user(client)
    response = client.get("/users/count")
    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_reset(client):
    _create_user(client)
    response = client.post("/users/reset")
    assert response.status_code == 200
    assert client.get("/users/count").json()["count"] == 0
