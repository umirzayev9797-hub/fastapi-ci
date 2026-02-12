from flask import Flask, request, make_response

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <title>CSP Demo</title>
</head>
<body>
 {user_input}
</body>
</html>
"""


# === CSP DECORATOR ===
def csp_protect(view):
    def wrapped(*args, **kwargs):
        resp = make_response(view(*args, **kwargs))

        # CSP политика:
        # - запрещает inline JS
        # - разрешает скрипты только с этого же origin
        # - запрещает <object>, <embed>, <applet>
        # - защита от base tag injection
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none';"
        )

        resp.headers["Content-Security-Policy"] = csp_policy

        return resp

    wrapped.__name__ = view.__name__
    return wrapped


# === ENDPOINT ===
@app.route("/")
@csp_protect
def index():
    user_input = request.args.get("q", "")

    html = HTML.format(user_input=user_input)
    return html


if __name__ == "__main__":
    app.run(debug=True)
