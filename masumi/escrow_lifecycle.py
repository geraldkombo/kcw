from __future__ import annotations

from enum import Enum
from typing import Any, Optional


class EscrowState(str, Enum):
    INITIATED = "initiated"
    LOCKED = "locked"
    SUBMITTED = "submitted"
    COMPLETED = "completed"
    REFUND_AUTHORIZED = "refund_authorized"


class EscrowLifecycle:
    """Escrow state machine for x402 micropayments."""

    VALID_TRANSITIONS: dict[EscrowState, list[EscrowState]] = {
        EscrowState.INITIATED: [EscrowState.LOCKED],
        EscrowState.LOCKED: [EscrowState.SUBMITTED, EscrowState.REFUND_AUTHORIZED],
        EscrowState.SUBMITTED: [EscrowState.COMPLETED, EscrowState.REFUND_AUTHORIZED],
        EscrowState.COMPLETED: [],
        EscrowState.REFUND_AUTHORIZED: [EscrowState.COMPLETED],
    }

    def __init__(self, escrow_id: str, amount_lovelace: int) -> None:
        self.escrow_id = escrow_id
        self.amount_lovelace = amount_lovelace
        self.state = EscrowState.INITIATED
        self.data_hash: Optional[str] = None

    def transition(self, target: EscrowState) -> None:
        allowed = self.VALID_TRANSITIONS.get(self.state, [])
        if target not in allowed:
            raise ValueError(f"Invalid transition: {self.state.value} -> {target.value}")
        self.state = target

    def to_dict(self) -> dict[str, Any]:
        return {
            "escrow_id": self.escrow_id,
            "amount_lovelace": self.amount_lovelace,
            "state": self.state.value,
            "data_hash": self.data_hash,
        }
