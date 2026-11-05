"""
The secure counterpart of examples/vulnerable-app/app.py.

Same endpoints, every bug fixed. Each comment names the bug it replaces.
"""

import ipaddress
import os
import socket
import sqlite3

from flask import Flask, request

app = Flask(__name__)

# FIX (hardcoded secret): the key comes from the environment. The app refuses
# to start without it instead of silently falling back to a default value.
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")
app.config["SECRET_KEY"] = SECRET_KEY


def get_db():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE users (name TEXT, email TEXT)")
    db.execute("INSERT INTO users VALUES ('alice', 'alice@example.com')")
    return db


@app.route("/health")
def health():
    return "ok"


@app.route("/users")
def users():
    # FIX (SQL injection): a parameterized query. The database driver sends
    # the value separately from the SQL, so it can never change the query.
    name = request.args.get("name", "")
    rows = get_db().execute(
        "SELECT name, email FROM users WHERE name = ?", (name,)
    ).fetchall()
    return {"users": rows}


@app.route("/ping")
def ping():
    # FIX (command injection): no shell at all. The input must parse as an IP
    # address, and only public addresses are allowed, so the endpoint cannot
    # be used to probe the internal network (SSRF).
    try:
        ip = ipaddress.ip_address(request.args.get("host", ""))
    except ValueError:
        return {"error": "host must be an IP address"}, 400
    if not ip.is_global:
        return {"error": "only public addresses are allowed"}, 400
    try:
        with socket.create_connection((str(ip), 443), timeout=2):
            reachable = True
    except OSError:
        reachable = False
    return {"host": str(ip), "reachable": reachable}


@app.route("/hello")
def hello():
    # FIX (template injection / XSS): user input is returned as JSON data,
    # never rendered as a template or HTML.
    name = request.args.get("name", "world")[:100]
    return {"message": f"Hello {name}"}


@app.route("/config", methods=["POST"])
def config():
    # FIX (unsafe deserialization): JSON can only describe plain data, never
    # Python objects.
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"error": "expected a JSON object"}, 400
    return {"keys": list(data.keys())}


if __name__ == "__main__":
    # FIX (debug mode): local development only, debugger off, localhost only.
    # In the container the app runs under gunicorn (see Dockerfile).
    app.run(host="127.0.0.1", port=8000, debug=False)
