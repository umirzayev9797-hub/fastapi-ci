import random
import factory
from faker import Faker

from app.models import Client, Parking
from app.extensions import db

fake = Faker()


# ---------------- CLIENT FACTORY ----------------

class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")

    # либо есть карта, либо нет
    credit_card = factory.LazyFunction(
        lambda: fake.credit_card_number() if random.choice([True, False]) else None
    )

    car_number = factory.Faker("bothify", text="??###??")


# ---------------- PARKING FACTORY ----------------

class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    address = factory.Faker("address")

    opened = factory.Faker("boolean")

    count_places = factory.Faker(
        "random_int",
        min=10,
        max=500
    )

    # доступные места = общее - случайное занятое
    @factory.lazy_attribute
    def count_available_places(self):
        taken = random.randint(0, self.count_places)
        return self.count_places - taken
