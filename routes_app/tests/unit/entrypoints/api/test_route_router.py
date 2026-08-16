AUTH_HEADER = {"Authorization": "Bearer some-token"}


def _create_route(client, flight_id="AA001"):
    return client.post(
        "/routes",
        json={
            "flightId": flight_id,
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "MIA",
            "destinyCountry": "USA",
            "bagCost": 50,
            "plannedStartDate": "2027-01-01T10:00:00",
            "plannedEndDate": "2027-01-01T15:00:00",
        },
        headers=AUTH_HEADER,
    )


def test_ping(client):
    response = client.get("/routes/ping")
    assert response.status_code == 200
    assert response.text == "pong"


def test_create_route_success(client):
    response = _create_route(client)
    assert response.status_code == 201
    assert "id" in response.json()


def test_create_route_missing_auth(client):
    response = client.post(
        "/routes",
        json={
            "flightId": "AA001",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "MIA",
            "destinyCountry": "USA",
            "bagCost": 50,
            "plannedStartDate": "2027-01-01T10:00:00",
            "plannedEndDate": "2027-01-01T15:00:00",
        },
    )
    assert response.status_code == 403


def test_create_route_duplicate_flight(client):
    _create_route(client)
    response = _create_route(client)
    assert response.status_code == 412


def test_create_route_invalid_dates(client):
    response = client.post(
        "/routes",
        json={
            "flightId": "BB002",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "MIA",
            "destinyCountry": "USA",
            "bagCost": 50,
            "plannedStartDate": "2027-01-01T15:00:00",
            "plannedEndDate": "2027-01-01T10:00:00",
        },
        headers=AUTH_HEADER,
    )
    assert response.status_code == 412


def test_list_routes(client):
    _create_route(client)
    response = client.get("/routes", headers=AUTH_HEADER)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_routes_filter_by_flight(client):
    _create_route(client, flight_id="AA001")
    _create_route(client, flight_id="BB002")
    response = client.get("/routes?flight=AA001", headers=AUTH_HEADER)
    assert len(response.json()) == 1


def test_get_route_success(client):
    created = _create_route(client).json()
    response = client.get(f"/routes/{created['id']}", headers=AUTH_HEADER)
    assert response.status_code == 200


def test_get_route_not_found(client):
    response = client.get("/routes/does-not-exist", headers=AUTH_HEADER)
    assert response.status_code == 404


def test_delete_route_success(client):
    created = _create_route(client).json()
    response = client.delete(f"/routes/{created['id']}", headers=AUTH_HEADER)
    assert response.status_code == 200


def test_delete_route_not_found(client):
    response = client.delete("/routes/does-not-exist", headers=AUTH_HEADER)
    assert response.status_code == 404


def test_count_routes(client):
    _create_route(client)
    response = client.get("/routes/count")
    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_reset(client):
    _create_route(client)
    response = client.post("/routes/reset")
    assert response.status_code == 200
    assert client.get("/routes/count").json()["count"] == 0
