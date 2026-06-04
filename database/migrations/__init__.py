from __future__ import annotations

import logging
import sqlite3
from importlib import resources
from pathlib import Path
from typing import Optional

logger = logging.getLogger("frk.db.migrations")

MIGRATIONS_TABLE = "schema_version"
MIGRATIONS_DIR = Path(__file__).parent


def _get_applied(conn: sqlite3.Connection) -> set[str]:
    cursor = conn.execute(
        f"SELECT name FROM {MIGRATIONS_TABLE} ORDER BY applied_at"
    )
    return {row[0] for row in cursor.fetchall()}


def _ensure_migrations_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        f"CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} ("
        "name TEXT PRIMARY KEY,"
        "applied_at TEXT NOT NULL DEFAULT (datetime('now'))"
        ")"
    )
    conn.commit()


def run_pending(conn: sqlite3.Connection) -> list[str]:
    _ensure_migrations_table(conn)
    applied = _get_applied(conn)

    migrations = sorted(
        p for p in MIGRATIONS_DIR.iterdir()
        if p.suffix == ".sql" and p.stem not in applied
    )

    if not migrations:
        return []

    applied_names = []
    for path in migrations:
        sql = path.read_text(encoding="utf-8")
        try:
            conn.executescript(sql)
            conn.execute(
                f"INSERT INTO {MIGRATIONS_TABLE} (name) VALUES (?)",
                (path.stem,),
            )
            conn.commit()
            applied_names.append(path.stem)
            logger.info("applied migration: %s", path.stem)
        except Exception:
            logger.exception("migration %s failed — rolling back", path.stem)
            conn.rollback()
            raise

    return applied_names
