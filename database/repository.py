from __future__ import annotations

import json
import logging
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from neo4j import AsyncGraphDatabase, exceptions as neo4j_exc
from config.settings import settings

logger = logging.getLogger("kcw.db")


class Repository:
    """Abstract interface for all repository implementations."""

    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...
    @property
    def connected(self) -> bool: ...

    def save_farmer(self, farmer: dict[str, Any]) -> dict[str, Any]: ...
    def get_farmer(self, farmer_id: str) -> Optional[dict[str, Any]]: ...
    def list_farmers(self) -> list[dict[str, Any]]: ...

    def save_loan(self, loan: dict[str, Any]) -> dict[str, Any]: ...
    def get_loan(self, loan_id: str) -> Optional[dict[str, Any]]: ...
    def list_loans(self) -> list[dict[str, Any]]: ...

    def save_pool(self, pool: dict[str, Any]) -> dict[str, Any]: ...
    def get_pool(self, pool_id: str) -> Optional[dict[str, Any]]: ...
    def list_pools(self) -> list[dict[str, Any]]: ...

    def record_audit(self, entry: dict[str, Any]) -> dict[str, Any]: ...
    def get_audit(self, farmer_id: str) -> list[dict[str, Any]]: ...
    def get_all_audit(self) -> list[dict[str, Any]]: ...


class SQLiteRepository(Repository):
    """File-backed SQLite repository for production use without Neo4j."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._path = Path(db_path or settings.data_dir / "kcw.db")
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
        self._connected = False

    async def connect(self) -> None:
        if self._connected:
            return
        try:
            self._conn = sqlite3.connect(str(self._path))
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
            self._create_tables()
            self._connected = True
            logger.info("connected to SQLite at %s", self._path)
        except Exception:
            logger.exception("failed to connect to SQLite at %s", self._path)
            raise

    def _create_tables(self) -> None:
        assert self._conn is not None
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS farmers (
                farmer_id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS loans (
                loan_id TEXT PRIMARY KEY,
                farmer_id TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS pools (
                pool_id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id TEXT,
                data TEXT NOT NULL,
                timestamp TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_loans_farmer ON loans(farmer_id);
            CREATE INDEX IF NOT EXISTS idx_audit_farmer ON audit_entries(farmer_id);
        """)
        self._conn.commit()

    async def disconnect(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None
            self._connected = False
            logger.info("disconnected from SQLite")

    @property
    def connected(self) -> bool:
        return self._connected

    def save_farmer(self, farmer: dict[str, Any]) -> dict[str, Any]:
        assert self._conn is not None
        farmer_id = farmer.get("farmer_id") or farmer.get("id", f"KCW-{uuid.uuid4().hex[:8].upper()}")
        farmer["farmer_id"] = farmer_id
        now = datetime.now(timezone.utc).isoformat()
        farmer.setdefault("created_at", now)
        farmer["updated_at"] = now
        self._conn.execute(
            "INSERT OR REPLACE INTO farmers (farmer_id, data, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (farmer_id, json.dumps(farmer, default=str), farmer.get("created_at", now), now),
        )
        self._conn.commit()
        return farmer

    def get_farmer(self, farmer_id: str) -> Optional[dict[str, Any]]:
        assert self._conn is not None
        row = self._conn.execute("SELECT data FROM farmers WHERE farmer_id = ?", (farmer_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def list_farmers(self) -> list[dict[str, Any]]:
        assert self._conn is not None
        rows = self._conn.execute("SELECT data FROM farmers ORDER BY created_at DESC").fetchall()
        return [json.loads(r[0]) for r in rows]

    def save_loan(self, loan: dict[str, Any]) -> dict[str, Any]:
        assert self._conn is not None
        loan_id = loan.get("loan_id") or f"LN-{uuid.uuid4().hex[:8].upper()}"
        loan["loan_id"] = loan_id
        now = datetime.now(timezone.utc).isoformat()
        loan.setdefault("created_at", now)
        loan["updated_at"] = now
        farmer_id = loan.get("farmer_id", "")
        self._conn.execute(
            "INSERT OR REPLACE INTO loans (loan_id, farmer_id, data, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (loan_id, farmer_id, json.dumps(loan, default=str), loan.get("created_at", now), now),
        )
        self._conn.commit()
        return loan

    def get_loan(self, loan_id: str) -> Optional[dict[str, Any]]:
        assert self._conn is not None
        row = self._conn.execute("SELECT data FROM loans WHERE loan_id = ?", (loan_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def list_loans(self) -> list[dict[str, Any]]:
        assert self._conn is not None
        rows = self._conn.execute("SELECT data FROM loans ORDER BY created_at DESC").fetchall()
        return [json.loads(r[0]) for r in rows]

    def save_pool(self, pool: dict[str, Any]) -> dict[str, Any]:
        assert self._conn is not None
        pool_id = pool.get("pool_id") or str(uuid.uuid4().hex[:8].upper())
        pool["pool_id"] = pool_id
        now = datetime.now(timezone.utc).isoformat()
        pool.setdefault("created_at", now)
        self._conn.execute(
            "INSERT OR REPLACE INTO pools (pool_id, data, created_at) VALUES (?, ?, ?)",
            (pool_id, json.dumps(pool, default=str), pool.get("created_at", now)),
        )
        self._conn.commit()
        return pool

    def get_pool(self, pool_id: str) -> Optional[dict[str, Any]]:
        assert self._conn is not None
        row = self._conn.execute("SELECT data FROM pools WHERE pool_id = ?", (pool_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def list_pools(self) -> list[dict[str, Any]]:
        assert self._conn is not None
        rows = self._conn.execute("SELECT data FROM pools ORDER BY created_at DESC").fetchall()
        return [json.loads(r[0]) for r in rows]

    def record_audit(self, entry: dict[str, Any]) -> dict[str, Any]:
        assert self._conn is not None
        entry["timestamp"] = entry.get("timestamp", datetime.now(timezone.utc).isoformat())
        self._conn.execute(
            "INSERT INTO audit_entries (farmer_id, data, timestamp) VALUES (?, ?, ?)",
            (entry.get("farmer_id", ""), json.dumps(entry, default=str), entry["timestamp"]),
        )
        self._conn.commit()
        return entry

    def get_audit(self, farmer_id: str) -> list[dict[str, Any]]:
        assert self._conn is not None
        rows = self._conn.execute(
            "SELECT data FROM audit_entries WHERE farmer_id = ? ORDER BY timestamp DESC", (farmer_id,)
        ).fetchall()
        return [json.loads(r[0]) for r in rows]

    def get_all_audit(self) -> list[dict[str, Any]]:
        assert self._conn is not None
        rows = self._conn.execute("SELECT data FROM audit_entries ORDER BY timestamp DESC").fetchall()
        return [json.loads(r[0]) for r in rows]


class InMemoryRepository(Repository):
    """Fallback in-memory repository for development and testing."""

    def __init__(self) -> None:
        self.farmers: dict[str, dict[str, Any]] = {}
        self.loans: dict[str, dict[str, Any]] = {}
        self.pools: dict[str, dict[str, Any]] = {}
        self.audit_entries: list[dict[str, Any]] = []

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        self.farmers.clear()
        self.loans.clear()
        self.pools.clear()
        self.audit_entries.clear()

    @property
    def connected(self) -> bool:
        return True

    def save_farmer(self, farmer: dict[str, Any]) -> dict[str, Any]:
        farmer_id = farmer.get("farmer_id") or farmer.get("id", str(len(self.farmers) + 1))
        farmer["farmer_id"] = farmer_id
        farmer["created_at"] = farmer.get("created_at", datetime.now(timezone.utc).isoformat())
        farmer["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.farmers[farmer_id] = farmer
        return farmer

    def get_farmer(self, farmer_id: str) -> Optional[dict[str, Any]]:
        return self.farmers.get(farmer_id)

    def list_farmers(self) -> list[dict[str, Any]]:
        return list(self.farmers.values())

    def save_loan(self, loan: dict[str, Any]) -> dict[str, Any]:
        loan_id = loan.get("loan_id") or str(len(self.loans) + 1)
        loan["loan_id"] = loan_id
        loan["created_at"] = loan.get("created_at", datetime.now(timezone.utc).isoformat())
        loan["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.loans[loan_id] = loan
        return loan

    def get_loan(self, loan_id: str) -> Optional[dict[str, Any]]:
        return self.loans.get(loan_id)

    def list_loans(self) -> list[dict[str, Any]]:
        return list(self.loans.values())

    def save_pool(self, pool: dict[str, Any]) -> dict[str, Any]:
        pool_id = pool.get("pool_id") or str(len(self.pools) + 1)
        pool["pool_id"] = pool_id
        pool["created_at"] = pool.get("created_at", datetime.now(timezone.utc).isoformat())
        self.pools[pool_id] = pool
        return pool

    def get_pool(self, pool_id: str) -> Optional[dict[str, Any]]:
        return self.pools.get(pool_id)

    def list_pools(self) -> list[dict[str, Any]]:
        return list(self.pools.values())

    def record_audit(self, entry: dict[str, Any]) -> dict[str, Any]:
        entry["timestamp"] = entry.get("timestamp", datetime.now(timezone.utc).isoformat())
        self.audit_entries.append(entry)
        return entry

    def get_audit(self, farmer_id: str) -> list[dict[str, Any]]:
        return [e for e in self.audit_entries if e.get("farmer_id") == farmer_id]

    def get_all_audit(self) -> list[dict[str, Any]]:
        return list(self.audit_entries)


class Neo4jRepository(Repository):
    """Neo4j-backed repository for production deployments with Neo4j."""

    def __init__(self) -> None:
        self._driver: Optional[Any] = None

    async def connect(self) -> None:
        if self._driver is not None:
            return
        try:
            self._driver = AsyncGraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password),
                max_connection_pool_size=settings.neo4j_max_connection_pool_size,
                connection_timeout=15,
            )
            await self._driver.verify_connectivity()
            logger.info("connected to Neo4j at %s", settings.neo4j_uri)
        except neo4j_exc.AuthError:
            logger.error("Neo4j authentication failed — check NEO4J_USER / NEO4J_PASSWORD")
            raise
        except neo4j_exc.ServiceUnavailable:
            logger.warning("Neo4j unreachable at %s", settings.neo4j_uri)
            self._driver = None
        except Exception:
            logger.exception("unexpected Neo4j connection error")
            self._driver = None

    async def disconnect(self) -> None:
        if self._driver is not None:
            await self._driver.close()
            self._driver = None
            logger.info("disconnected from Neo4j")

    @property
    def connected(self) -> bool:
        return self._driver is not None

    async def run(self, query: str, params: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        if self._driver is None:
            return []
        try:
            async with self._driver.session() as session:
                result = await session.run(query, params or {})
                records = await result.data()
                return records
        except neo4j_exc.ServiceUnavailable:
            logger.warning("Neo4j connection lost — query skipped")
            return []
        except Exception:
            logger.exception("Neo4j query failed")
            return []

    async def run_transaction(self, queries: list[tuple[str, Optional[dict[str, Any]]]]) -> list[list[dict[str, Any]]]:
        if self._driver is None:
            return []
        try:
            async with self._driver.session() as session:
                results = []
                async with session.begin_transaction() as tx:
                    for query, params in queries:
                        result = await tx.run(query, params or {})
                        records = await result.data()
                        results.append(records)
                    await tx.commit()
                return results
        except Exception:
            logger.exception("Neo4j transaction failed")
            return []

    def save_farmer(self, farmer: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("Neo4jRepository uses Cypher queries; use run() instead")

    def get_farmer(self, farmer_id: str) -> Optional[dict[str, Any]]:
        raise NotImplementedError

    def list_farmers(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def save_loan(self, loan: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def get_loan(self, loan_id: str) -> Optional[dict[str, Any]]:
        raise NotImplementedError

    def list_loans(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def save_pool(self, pool: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def get_pool(self, pool_id: str) -> Optional[dict[str, Any]]:
        raise NotImplementedError

    def list_pools(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def record_audit(self, entry: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def get_audit(self, farmer_id: str) -> list[dict[str, Any]]:
        raise NotImplementedError

    def get_all_audit(self) -> list[dict[str, Any]]:
        raise NotImplementedError


def create_repository() -> Repository:
    """Factory: returns SQLiteRepository, Neo4jRepository, or InMemoryRepository based on DATABASE_URL."""
    db_url = settings.database_url
    if db_url.startswith("sqlite"):
        path = db_url.replace("sqlite:///", "")
        return SQLiteRepository(db_path=path)
    if db_url.startswith("neo4j"):
        return Neo4jRepository()
    return InMemoryRepository()
