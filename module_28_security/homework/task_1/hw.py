from flask import Flask, request, jsonify, make_response
from functools import wraps

app = Flask(__name__)

# === CORS CONFIG (whitelist, не wildcard!) ===
ALLOWED_ORIGINS = {
    "https://example.com",   # можно заменить на свой фронт
}

ALLOWED_METHODS = ["GET", "POST"]
ALLOWED_HEADERS = ["X-My-Fancy-Header", "Content-Type"]

ALLOW_CREDENTIALS = "true"  # строка по стандарту CORS


# === CORS DECORATOR ===
def cors_protect(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        origin = request.headers.get("Origin")

        # Если origin не из whitelist — не добавляем CORS-хедеры
        # (браузер сам заблокирует)
        if origin not in ALLOWED_ORIGINS:
            if request.method == "OPTIONS":
                return make_response("", 403)
            return view(*args, **kwargs)

        # --- PREFLIGHT ---
        if request.method == "OPTIONS":
            resp = make_response("", 204)
        else:
            resp = make_response(view(*args, **kwargs))

        # --- CORS HEADERS ---
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Access-Control-Allow-Methods"] = ", ".join(ALLOWED_METHODS)
        resp.headers["Access-Control-Allow-Headers"] = ", ".join(ALLOWED_HEADERS)
        resp.headers["Access-Control-Allow-Credentials"] = ALLOW_CREDENTIALS

        # Best practice (OWASP / MDN)
        resp.headers["Vary"] = "Origin"

        return resp

    return wrapped


# === ENDPOINTS ===

@app.route("/resource", methods=["GET"])
@cors_protect
def get_resource():
    return jsonify({
        "status": "success",
        "method": "GET",
        "data": "Some protected data"
    })


@app.route("/resource", methods=["POST"])
@cors_protect
def post_resource():
    payload = request.get_json(silent=True) or {}

    return jsonify({
        "status": "success",
        "method": "POST",
        "received": payload
    })


# === PREFLIGHT HANDLER ===
@app.route("/resource", methods=["OPTIONS"])
@cors_protect
def options_resource():
    return make_response("", 204)


if __name__ == "__main__":
    app.run(debug=True)
