from app.models import Client
from app.extensions import db
from tests.factories import ClientFactory


def test_create_client_factory(app):
    with app.app_context():
        before = Client.query.count()

        client = ClientFactory()

        after = Client.query.count()

        assert client.id is not None
        assert after == before + 1
