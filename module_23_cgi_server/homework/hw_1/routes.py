import json
from app_framework import WSGIApp

app = WSGIApp()

@app.route("/hello")
def say_hello():
    return json.dumps({"response": "Hello, world!"}, indent=4)

@app.route("/hello/<name>")
def say_hello_with_name(name: str):
    return json.dumps({"response": f"Hello, {name}!"}, indent=4)