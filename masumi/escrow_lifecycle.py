"""Escrow lifecycle state machine for KCW loan disbursement.
Mirrors Masumi Payment Service states with TxPipe-audited contracts.
"""

from datetime import datetime, timezone
from enum import Enum


class EscrowState(str, Enum):
    FUNDS_LOCKING_REQUESTED = "FundsLockingRequested"
    FUNDS_LOCKED = "FundsLocked"
    RESULT_SUBMITTED = "ResultSubmitted"
    COMPLETED = "Completed"
    REFUND_REQUESTED = "RefundRequested"
    REFUND_AUTHORIZED = "RefundAuthorized"
    REFUNDED = "Refunded"
    DISPUTED = "Disputed"


# Valid transitions
ESCROW_TRANSITIONS = {
    EscrowState.FUNDS_LOCKING_REQUESTED: [EscrowState.FUNDS_LOCKED],
    EscrowState.FUNDS_LOCKED: [
        EscrowState.RESULT_SUBMITTED,
        EscrowState.REFUND_REQUESTED,
    ],
    EscrowState.RESULT_SUBMITTED: [
        EscrowState.COMPLETED,
        EscrowState.REFUND_AUTHORIZED,
        EscrowState.DISPUTED,
    ],
    EscrowState.COMPLETED: [],
    EscrowState.REFUND_REQUESTED: [EscrowState.REFUNDED, EscrowState.DISPUTED],
    EscrowState.REFUND_AUTHORIZED: [EscrowState.REFUNDED],
    EscrowState.REFUNDED: [],
    EscrowState.DISPUTED: [EscrowState.REFUNDED, EscrowState.COMPLETED],
}


class EscrowLifecycle:
    """Tracks and validates escrow state transitions."""

    def __init__(self, escrow_id: str, initial_state: EscrowState = EscrowState.FUNDS_LOCKING_REQUESTED):
        self.escrow_id = escrow_id
        self._state = initial_state
        self.history = [{"state": initial_state.value, "timestamp": datetime.now(timezone.utc).isoformat()}]

    @property
    def state(self) -> EscrowState:
        return self._state

    @state.setter
    def state(self, new_state: EscrowState):
        allowed = ESCROW_TRANSITIONS.get(self._state, [])
        if new_state not in allowed:
            raise ValueError(
                f"Invalid transition: {self._state.value} -> {new_state.value}. "
                f"Allowed: {[s.value for s in allowed]}"
            )
        self._state = new_state
        self.history.append({
            "state": new_state.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def to_dict(self) -> dict:
        return {
            "escrow_id": self.escrow_id,
            "current_state": self._state.value,
            "history": self.history,
        }
