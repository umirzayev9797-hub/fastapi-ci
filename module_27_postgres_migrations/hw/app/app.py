from flask import Flask
import psycopg2
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Flask + Gunicorn + Postgres работает!"

