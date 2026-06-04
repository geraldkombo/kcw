from __future__ import annotations

import argparse
import logging
import sqlite3
from pathlib import Path

from database.migrations import run_pending

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("frk.db.migrations.cli")


def main() -> None:
    parser = argparse.ArgumentParser(description="KCW database migrations")
    parser.add_argument("--db", default="data/frk.db", help="SQLite database path")
    args = parser.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    try:
        applied = run_pending(conn)
        if applied:
            logger.info("applied %d migration(s): %s", len(applied), ", ".join(applied))
        else:
            logger.info("schema is up to date — no pending migrations")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
