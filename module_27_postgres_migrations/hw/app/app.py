from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy import func
import requests
import random

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# ================= MODELS =================

class Coffee(db.Model):
    __tablename__ = "coffee"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200))
    description = db.Column(db.String(200))
    reviews = db.Column(ARRAY(db.String))


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    has_sale = db.Column(db.Boolean)
    address = db.Column(JSON)

    coffee_id = db.Column(db.Integer, db.ForeignKey("coffee.id"))
    coffee = db.relationship("Coffee")


# ================= INIT DB =================

with app.app_context():
    db.create_all()


# ================= SEED DATA =================

@app.before_first_request
def seed():

    if Coffee.query.first():
        return

    # Coffee
    r = requests.get("https://dummyjson.com/products/search?q=coffee").json()
    p = r["products"][0]

    reviews = [rv["comment"] for rv in p.get("reviews", []) if "comment" in rv]

    coffee = Coffee(
        title=p["title"],
        category=p["category"],
        description=p["description"],
        reviews=reviews
    )

    db.session.add(coffee)
    db.session.commit()

    # Users
    ur = requests.get("https://dummyjson.com/users?limit=10").json()

    for u in ur["users"]:
        user = User(
            name=u["firstName"],
            has_sale=random.choice([True, False]),
            address=u["address"],
            coffee_id=coffee.id
        )
        db.session.add(user)

    db.session.commit()


# ================= ROUTES =================

@app.route("/add_user", methods=["POST"])
def add_user():

    data = request.json

    user = User(
        name=data["name"],
        has_sale=data.get("has_sale", False),
        address=data.get("address"),
        coffee_id=data["coffee_id"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "user": user.name,
        "coffee": user.coffee.title
    })


@app.route("/coffee_search")
def coffee_search():

    q = request.args.get("q")

    res = Coffee.query.filter(
        func.to_tsvector("english", Coffee.title).match(q)
    ).all()

    return jsonify([c.title for c in res])


@app.route("/unique_reviews")
def unique_reviews():

    reviews = []
    for c in Coffee.query.all():
        if c.reviews:
            reviews.extend(c.reviews)

    return jsonify(list(set(reviews)))


@app.route("/users_by_country")
def users_by_country():

    country = request.args.get("country")

    users = User.query.filter(
        User.address["country"].astext == country
    ).all()

    return jsonify([u.name for u in users])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
