def _create_offer(client, post_id="post-1", owner="user-1", size="MEDIUM", offer=100.0):
    return client.post(
        "/offers",
        json={
            "postId": post_id,
            "userId": owner,
            "description": "Paquete de prueba",
            "size": size,
            "fragile": False,
            "offer": offer,
        },
    )


def test_ping(client):
    response = client.get("/offers/ping")
    assert response.status_code == 200
    assert response.text == "pong"


def test_create_offer_success(client):
    response = _create_offer(client)
    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert "createdAt" in body


def test_create_offer_invalid_size(client):
    response = _create_offer(client, size="HUGE")
    assert response.status_code == 412


def test_create_offer_negative_amount(client):
    response = _create_offer(client, offer=-10)
    assert response.status_code == 412


def test_list_offers(client):
    _create_offer(client)
    response = client.get("/offers")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_offers_filter_by_post(client):
    _create_offer(client, post_id="post-1")
    _create_offer(client, post_id="post-2")
    response = client.get("/offers?post=post-1")
    assert len(response.json()) == 1


def test_list_offers_filter_by_owner(client):
    _create_offer(client, owner="user-1")
    _create_offer(client, owner="user-2")
    response = client.get("/offers?owner=user-2")
    assert len(response.json()) == 1


def test_get_offer_success(client):
    created = _create_offer(client).json()
    response = client.get(f"/offers/{created['id']}")
    assert response.status_code == 200


def test_get_offer_not_found(client):
    response = client.get("/offers/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_get_offer_invalid_id_format(client):
    response = client.get("/offers/does-not-exist")
    assert response.status_code == 400


def test_delete_offer_success(client):
    created = _create_offer(client).json()
    response = client.delete(f"/offers/{created['id']}")
    assert response.status_code == 200


def test_delete_offer_not_found(client):
    response = client.delete("/offers/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_delete_offer_invalid_id_format(client):
    response = client.delete("/offers/does-not-exist")
    assert response.status_code == 400


def test_count_offers(client):
    _create_offer(client)
    response = client.get("/offers/count")
    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_reset(client):
    _create_offer(client)
    response = client.post("/offers/reset")
    assert response.status_code == 200
    assert client.get("/offers/count").json()["count"] == 0
