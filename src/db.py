import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "requests.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Создаёт БД и заливает данные только если файла ещё нет."""
    if DB_PATH.exists():
        print(f"БД уже существует: {DB_PATH}")
        return

    schema = (BASE_DIR / "db" / "schema.sql").read_text(encoding="utf-8")
    seed = (BASE_DIR / "db" / "seed.sql").read_text(encoding="utf-8")

    conn = get_connection()
    conn.executescript(schema)
    conn.executescript(seed)
    conn.commit()
    conn.close()
    print(f"БД создана и заполнена: {DB_PATH}")