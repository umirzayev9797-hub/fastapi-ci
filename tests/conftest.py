import pytest
from datetime import datetime, timedelta

from app import create_app
from app.extensions import db as _db
from app.models import Client, Parking, ClientParking


# ---------- APP FIXTURE ----------
@pytest.fixture
def app():
    app = create_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        _db.create_all()

        # --- тестовые данные ---
        client = Client(
            name="Test",
            surname="User",
            credit_card="1111",
            car_number="A111AA"
        )

        parking = Parking(
            address="Test address",
            opened=True,
            count_places=5,
            count_available_places=5,
        )

        _db.session.add_all([client, parking])
        _db.session.commit()

        # лог парковки
        log = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in=datetime.utcnow() - timedelta(hours=1),
            time_out=datetime.utcnow(),
        )

        _db.session.add(log)
        _db.session.commit()

        yield app

        _db.session.remove()
        _db.drop_all()


# ---------- DB FIXTURE ----------
@pytest.fixture
def db(app):
    return _db


# ---------- CLIENT FIXTURE ----------
@pytest.fixture
def client(app):
    return app.test_client()
