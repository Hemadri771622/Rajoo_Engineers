# app/services/db_service.py

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "instance" / "blownfilm.db"


def get_db():
    """Return SQLite connection"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if missing"""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS machine_overview (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_set_output REAL,
            total_actual_output REAL,
            density REAL,
            gsm REAL,
            lay_flat REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("[DB] Initialized")


def get_updates():
    """Return latest machine overview snapshot"""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            total_set_output,
            total_actual_output,
            density,
            gsm,
            lay_flat,
            timestamp
        FROM machine_overview
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()

    return dict(row) if row else {}
