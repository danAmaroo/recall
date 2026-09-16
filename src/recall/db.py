from pathlib import Path
import sqlite3
from importlib.resources import files


def db_path() -> Path:
    path = Path.home() / ".local" / "share" / "recall" / "recall.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def connect(path: Path | str | None = None) -> sqlite3.Connection:
    if path is None:
        path = db_path()

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA trusted_schema = ON")

    schema = files("recall").joinpath("schema.sql").read_text()
    conn.executescript(schema)

    return conn