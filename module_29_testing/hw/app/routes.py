from datetime import datetime

from flask import Blueprint, request, jsonify

from .extensions import db
from .models import Client, Parking, ClientParking

bp = Blueprint("api", __name__)


# ---------------- CLIENTS ----------------

@bp.get("/clients")
def list_clients():
    clients = Client.query.all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "surname": c.surname,
            "credit_card": c.credit_card,
            "car_number": c.car_number,
        }
        for c in clients
    ])


@bp.get("/clients/<int:client_id>")
def get_client(client_id):
    client = Client.query.get_or_404(client_id)

    return jsonify({
        "id": client.id,
        "name": client.name,
        "surname": client.surname,
        "credit_card": client.credit_card,
        "car_number": client.car_number,
    })


@bp.post("/clients")
def create_client():
    data = request.get_json()

    client = Client(
        name=data["name"],
        surname=data["surname"],
        credit_card=data.get("credit_card"),
        car_number=data.get("car_number"),
    )

    db.session.add(client)
    db.session.commit()

    return jsonify({"id": client.id}), 201


# ---------------- PARKINGS ----------------

@bp.post("/parkings")
def create_parking():
    data = request.get_json()

    parking = Parking(
        address=data["address"],
        opened=data.get("opened", True),
        count_places=data["count_places"],
        count_available_places=data["count_places"],
    )

    db.session.add(parking)
    db.session.commit()

    return jsonify({"id": parking.id}), 201


# ---------------- ENTRY (ЗАЕЗД) ----------------

@bp.post("/client_parkings")
def enter_parking():
    data = request.get_json()

    client = Client.query.get_or_404(data["client_id"])
    parking = Parking.query.get_or_404(data["parking_id"])

    if not parking.opened:
        return jsonify({"error": "Parking closed"}), 400

    if parking.count_available_places <= 0:
        return jsonify({"error": "No free places"}), 400

    existing = ClientParking.query.filter_by(
        client_id=client.id,
        parking_id=parking.id,
        time_out=None
    ).first()

    if existing:
        return jsonify({"error": "Client already inside"}), 400

    record = ClientParking(
        client_id=client.id,
        parking_id=parking.id,
        time_in=datetime.utcnow(),
    )

    parking.count_available_places -= 1

    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Entry recorded"}), 201


# ---------------- EXIT (ВЫЕЗД) ----------------

@bp.delete("/client_parkings")
def exit_parking():
    data = request.get_json()

    client = Client.query.get_or_404(data["client_id"])
    parking = Parking.query.get_or_404(data["parking_id"])

    record = ClientParking.query.filter_by(
        client_id=client.id,
        parking_id=parking.id,
        time_out=None
    ).first()

    if not record:
        return jsonify({"error": "Client not on parking"}), 400

    if not client.credit_card:
        return jsonify({"error": "No credit card"}), 400

    record.time_out = datetime.utcnow()
    parking.count_available_places += 1

    # ---- простая логика оплаты ----
    duration = (record.time_out - record.time_in).total_seconds() / 60
    price = round(duration * 0.05, 2)  # 0.05 за минуту

    db.session.commit()

    return jsonify({
        "message": "Exit recorded",
        "duration_min": round(duration, 1),
        "charged": price
    })
