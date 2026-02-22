#!/usr/bin/env python3
"""CGI script for logging multiplication practice session data to SQLite."""

import json
import os
import sqlite3
import sys
import traceback

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "multiplication_practice.sqlite")

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    user TEXT,
    ip_address TEXT,
    session_start TEXT,
    session_end TEXT,
    session_duration REAL,
    mode TEXT,
    factor INTEGER
);
CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    problem_number INTEGER,
    problem TEXT,
    submitted_answer TEXT,
    correct INTEGER,
    time_to_solve REAL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
"""


def init_db(conn):
    conn.executescript(SCHEMA)
    conn.commit()


def respond(status_code, body):
    reason = {200: "OK", 400: "Bad Request", 500: "Internal Server Error"}.get(status_code, "Unknown")
    print(f"Status: {status_code} {reason}")
    print("Content-Type: application/json")
    print("Access-Control-Allow-Origin: *")
    print("Access-Control-Allow-Methods: POST, OPTIONS")
    print("Access-Control-Allow-Headers: Content-Type")
    print()
    print(json.dumps(body))


def handle_options():
    print("Status: 204 No Content")
    print("Access-Control-Allow-Origin: *")
    print("Access-Control-Allow-Methods: POST, OPTIONS")
    print("Access-Control-Allow-Headers: Content-Type")
    print()


def main():
    method = os.environ.get("REQUEST_METHOD", "GET")

    if method == "OPTIONS":
        handle_options()
        return

    if method != "POST":
        respond(400, {"error": "Only POST is supported"})
        return

    try:
        content_length = int(os.environ.get("CONTENT_LENGTH", 0))
        raw = sys.stdin.read(content_length)
        data = json.loads(raw)
    except Exception as e:
        respond(400, {"error": f"Invalid JSON: {e}"})
        return

    session = data.get("session")
    problems = data.get("problems", [])

    if not session or not session.get("session_id"):
        respond(400, {"error": "Missing session data"})
        return

    ip_address = os.environ.get("REMOTE_ADDR", "unknown")

    try:
        conn = sqlite3.connect(DB_PATH)
        init_db(conn)

        conn.execute(
            """INSERT OR REPLACE INTO sessions
               (session_id, user, ip_address, session_start, session_end,
                session_duration, mode, factor)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session.get("session_id"),
                session.get("user"),
                ip_address,
                session.get("session_start"),
                session.get("session_end"),
                session.get("session_duration"),
                session.get("mode"),
                session.get("factor"),
            ),
        )

        for p in problems:
            conn.execute(
                """INSERT INTO problems
                   (session_id, problem_number, problem, submitted_answer, correct, time_to_solve)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    session.get("session_id"),
                    p.get("problem_number"),
                    p.get("problem"),
                    str(p.get("submitted_answer", "")),
                    1 if p.get("correct") else 0,
                    p.get("time_to_solve"),
                ),
            )

        conn.commit()
        conn.close()
        respond(200, {"status": "ok"})

    except Exception as e:
        respond(500, {"error": str(e), "trace": traceback.format_exc()})


main()
