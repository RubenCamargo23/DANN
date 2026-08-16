def _create_post(client, route_id="route-1", owner="user-1", expire="2027-01-01T10:00:00"):
    return client.post(
        "/posts",
        json={"routeId": route_id, "expireAt": expire, "userId": owner},
    )


def test_ping(client):
    response = client.get("/posts/ping")
    assert response.status_code == 200
    assert response.text == "pong"


def test_create_post_success(client):
    response = _create_post(client)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert "createdAt" in body


def test_create_post_invalid_expire_date(client):
    response = _create_post(client, expire="2000-01-01T10:00:00")
    assert response.status_code == 412


def test_list_posts(client):
    _create_post(client)
    response = client.get("/posts")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_posts_filter_by_route(client):
    _create_post(client, route_id="route-1")
    _create_post(client, route_id="route-2")
    response = client.get("/posts?route=route-1")
    assert len(response.json()) == 1


def test_list_posts_filter_by_owner(client):
    _create_post(client, owner="user-1")
    _create_post(client, owner="user-2")
    response = client.get("/posts?owner=user-2")
    assert len(response.json()) == 1


def test_list_posts_filter_by_expire(client):
    _create_post(client, expire="2027-01-01T10:00:00")
    response = client.get("/posts?expire=false")
    assert len(response.json()) == 1
    expired = client.get("/posts?expire=true")
    assert len(expired.json()) == 0


def test_get_post_success(client):
    created = _create_post(client).json()
    response = client.get(f"/posts/{created['id']}")
    assert response.status_code == 200


def test_get_post_not_found(client):
    response = client.get("/posts/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_get_post_invalid_id_format(client):
    response = client.get("/posts/does-not-exist")
    assert response.status_code == 400


def test_delete_post_success(client):
    created = _create_post(client).json()
    response = client.delete(f"/posts/{created['id']}")
    assert response.status_code == 200


def test_delete_post_not_found(client):
    response = client.delete("/posts/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_delete_post_invalid_id_format(client):
    response = client.delete("/posts/does-not-exist")
    assert response.status_code == 400


def test_count_posts(client):
    _create_post(client)
    response = client.get("/posts/count")
    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_reset(client):
    _create_post(client)
    response = client.post("/posts/reset")
    assert response.status_code == 200
    assert client.get("/posts/count").json()["count"] == 0
