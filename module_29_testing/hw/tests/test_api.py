import pytest
from app.models import Parking, ClientParking
from app.extensions import db


# ---------------- GET TESTS ----------------

@pytest.mark.parametrize("url", [
    "/clients",
    "/clients/1",
])
def test_get_methods(client, url):
    resp = client.get(url)
    assert resp.status_code == 200


# ---------------- CREATE CLIENT ----------------

def test_create_client(client):
    resp = client.post("/clients", json={
        "name": "Ivan",
        "surname": "Petrov",
        "credit_card": "2222",
        "car_number": "B222BB"
    })

    assert resp.status_code == 201


# ---------------- CREATE PARKING ----------------

def test_create_parking(client):
    resp = client.post("/parkings", json={
        "address": "New",
        "count_places": 10
    })

    assert resp.status_code == 201


# ---------------- ENTRY ----------------

@pytest.mark.parking
def test_enter_parking(client, app):
    with app.app_context():
        parking_before = Parking.query.get(1).count_available_places

    resp = client.post("/client_parkings", json={
        "client_id": 1,
        "parking_id": 1
    })

    assert resp.status_code == 201

    with app.app_context():
        parking_after = Parking.query.get(1).count_available_places

    assert parking_after == parking_before - 1


# ---------------- EXIT ----------------

@pytest.mark.parking
def test_exit_parking(client, app):
    # сначала заезд
    client.post("/client_parkings", json={
        "client_id": 1,
        "parking_id": 1
    })

    with app.app_context():
        parking_before = Parking.query.get(1).count_available_places

    resp = client.delete("/client_parkings", json={
        "client_id": 1,
        "parking_id": 1
    })

    assert resp.status_code == 200

    data = resp.get_json()
    assert data["charged"] >= 0

    with app.app_context():
        parking_after = Parking.query.get(1).count_available_places

        record = ClientParking.query.filter_by(
            client_id=1,
            parking_id=1
        ).order_by(ClientParking.id.desc()).first()

    assert parking_after == parking_before + 1
    assert record.time_out >= record.time_in


# ---------------- EXTRA TESTS (плюс к оценке) ----------------

def test_no_free_places(client, app):
    with app.app_context():
        p = Parking.query.get(1)
        p.count_available_places = 0
        db.session.commit()

    resp = client.post("/client_parkings", json={
        "client_id": 1,
        "parking_id": 1
    })

    assert resp.status_code == 400


def test_exit_without_card(client, app):
    from app.models import Client

    with app.app_context():
        c = Client.query.get(1)
        c.credit_card = None
        db.session.commit()

    client.post("/client_parkings", json={
        "client_id": 1,
        "parking_id": 1
    })

    resp = client.delete("/client_parkings", json={
        "client_id": 1,
        "parking_id": 1
    })

    assert resp.status_code == 400
