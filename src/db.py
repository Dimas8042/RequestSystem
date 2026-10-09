import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "requests.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    schema = (Path(__file__).resolve().parent.parent / "db" / "schema.sql").read_text(encoding="utf-8")
    seed = (Path(__file__).resolve().parent.parent / "db" / "seed.sql").read_text(encoding="utf-8")
    conn = get_connection()
    conn.executescript(schema)
    conn.executescript(seed)
    conn.commit()
    conn.close()