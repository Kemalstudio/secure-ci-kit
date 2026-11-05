"""
INTENTIONALLY VULNERABLE APPLICATION. DO NOT DEPLOY.

Every endpoint here contains a classic security bug, so that the scanners in
secure-ci-kit have something real to find. The fixed version of each bug is in
examples/secure-app/app.py, with the same endpoint names.
"""

import os
import sqlite3

import yaml
from flask import Flask, request, render_template_string

app = Flask(__name__)

# BUG: hardcoded secret. Anyone with read access to the repo (or its history)
# can sign session cookies. The value is fake and has never been used anywhere.
SECRET_KEY = "Zq8vT3xLp7Rk2Wm9Nf4Hj6Bd1Yc5Gs0E"
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
    # BUG: SQL injection. Try /users?name=' OR '1'='1
    name = request.args.get("name", "")
    query = f"SELECT name, email FROM users WHERE name = '{name}'"
    rows = get_db().execute(query).fetchall()
    return {"users": rows}


@app.route("/ping")
def ping():
    # BUG: command injection. Try /ping?host=127.0.0.1;cat /etc/passwd
    host = request.args.get("host", "127.0.0.1")
    os.system("ping -c 1 " + host)
    return "done"


@app.route("/hello")
def hello():
    # BUG: server-side template injection / XSS. Try /hello?name={{7*7}}
    name = request.args.get("name", "world")
    return render_template_string("<h1>Hello " + name + "</h1>")


@app.route("/config", methods=["POST"])
def config():
    # BUG: unsafe deserialization. yaml.load with the full loader can build
    # arbitrary Python objects from attacker-controlled input.
    data = yaml.load(request.data, Loader=yaml.Loader)
    return {"keys": list(data.keys())}


if __name__ == "__main__":
    # BUG: debug mode exposes the Werkzeug debugger (remote code execution),
    # and 0.0.0.0 makes it reachable from the network.
    app.run(host="0.0.0.0", port=5000, debug=True)
