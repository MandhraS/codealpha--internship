import os
import secrets
import sqlite3
from datetime import datetime, timezone
from urllib.parse import urlparse

from flask import Flask, jsonify, redirect, render_template, request, url_for


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "urls.db")


app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT NOT NULL UNIQUE,
                long_url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                clicks INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()


with app.app_context():
    init_db()


def normalize_url(url):
    url = url.strip()
    parsed = urlparse(url)

    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return None

    return url


def generate_short_code(length=6):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def create_unique_short_code():
    with get_db_connection() as conn:
        while True:
            short_code = generate_short_code()
            existing = conn.execute(
                "SELECT 1 FROM urls WHERE short_code = ?", (short_code,)
            ).fetchone()
            if existing is None:
                return short_code


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json(silent=True) or {}
    long_url = normalize_url(data.get("long_url", ""))

    if long_url is None:
        return jsonify({"error": "Please enter a valid http or https URL."}), 400

    short_code = create_unique_short_code()
    created_at = datetime.now(timezone.utc).isoformat()

    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO urls (short_code, long_url, created_at) VALUES (?, ?, ?)",
            (short_code, long_url, created_at),
        )
        conn.commit()

    short_url = url_for("redirect_to_url", short_code=short_code, _external=True)

    return jsonify(
        {
            "short_code": short_code,
            "short_url": short_url,
            "long_url": long_url,
        }
    ), 201


@app.route("/<short_code>")
def redirect_to_url(short_code):
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT long_url FROM urls WHERE short_code = ?", (short_code,)
        ).fetchone()

        if row is None:
            return render_template("404.html", short_code=short_code), 404

        conn.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,)
        )
        conn.commit()

    return redirect(row["long_url"])


@app.route("/api/stats/<short_code>")
def url_stats(short_code):
    with get_db_connection() as conn:
        row = conn.execute(
            """
            SELECT short_code, long_url, created_at, clicks
            FROM urls
            WHERE short_code = ?
            """,
            (short_code,),
        ).fetchone()

    if row is None:
        return jsonify({"error": "Short URL not found."}), 404

    return jsonify(dict(row))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
