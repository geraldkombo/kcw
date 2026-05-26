"""Audit trail and reporting service. Maintains immutable records
of all credit decisions, V&V checks, and escrow transactions
for Agusto rating agency compliance.
"""

from datetime import datetime, timezone
from typing import Any, Optional


class AuditTrail:
    """In-memory audit trail. In production, persists to both Neo4j
    (Reasoning Memory) and Cardano (Masumi Decision Logging).
    """

    def __init__(self):
        self._entries: list[dict] = []

    def record(
        self,
        event_type: str,
        actor: str,
        farmer_id: str,
        data: dict[str, Any],
        verification_hash: Optional[str] = None,
    ):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "actor": actor,
            "farmer_id": farmer_id,
            "data": data,
            "verification_hash": verification_hash or "",
        }
        self._entries.append(entry)
        return entry

    def get_history(self, farmer_id: str) -> list[dict]:
        return [
            e for e in self._entries if e["farmer_id"] == farmer_id
        ]

    def get_all(self) -> list[dict]:
        return list(self._entries)

    def count(self) -> int:
        return len(self._entries)
