from __future__ import annotations

from typing import Any


class InputSchema:
    """MIP-003 input schema for escrow endpoints."""

    def __init__(self, action: str, payload: dict[str, Any]) -> None:
        self.action = action
        self.payload = payload

    def to_dict(self) -> dict[str, Any]:
        return {"action": self.action, "payload": self.payload}


def generate_mip003_endpoints(base_url: str) -> list[dict[str, str]]:
    """Generate MIP-003 compliant endpoint definitions."""
    return [
        {"path": f"{base_url}/escrow/initiate", "method": "POST", "description": "Initiate escrow"},
        {"path": f"{base_url}/escrow/lock", "method": "POST", "description": "Lock funds in escrow"},
        {"path": f"{base_url}/escrow/submit", "method": "POST", "description": "Submit data hash"},
        {"path": f"{base_url}/escrow/complete", "method": "POST", "description": "Complete escrow"},
        {"path": f"{base_url}/escrow/refund", "method": "POST", "description": "Refund escrow"},
    ]
