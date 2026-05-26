"""Masumi x402 Protocol Client for Cardano testnet.
HTTP 402 Payment Required as a machine-to-machine payment gateway.
Cardano x402 spec merged April 23, 2026.
"""

import os
import json
import httpx
from typing import Optional
from enum import Enum


class EscrowState(str, Enum):
    funds_locking_requested = "FundsLockingRequested"
    funds_locked = "FundsLocked"
    result_submitted = "ResultSubmitted"
    completed = "Completed"
    refunded = "Refunded"
    disputed = "Disputed"


MASUMI_API_URL = "https://payment-service.masumi.network"


class MasumiX402Client:
    """Handles x402 payment initiation, escrow lifecycle, and settlement."""

    def __init__(self, api_url: Optional[str] = None):
        self.api_url = api_url or os.getenv(
            "MASUMI_API_URL", MASUMI_API_URL
        )
        self.wallet_address = os.getenv("MASUMI_WALLET_ADDRESS", "")
        self.network = os.getenv("CARDANO_NETWORK", "preprod")
        self._client = httpx.AsyncClient(
            base_url=self.api_url, timeout=30.0
        )

    async def close(self):
        await self._client.aclose()

    async def create_escrow(self, amount_lovelace: int, metadata: dict) -> dict:
        """POST /purchase — initiate FundsLockingRequested."""
        payload = {
            "receiver_address": self.wallet_address,
            "amount": {"unit": "lovelace", "quantity": str(amount_lovelace)},
            "network": self.network,
            "metadata": metadata,
        }
        resp = await self._client.post("/purchase", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def check_escrow_status(self, escrow_id: str) -> EscrowState:
        """GET /purchase/{id} — check current escrow state."""
        resp = await self._client.get(f"/purchase/{escrow_id}")
        resp.raise_for_status()
        data = resp.json()
        return EscrowState(data.get("state", "FundsLockingRequested"))

    async def submit_result(self, escrow_id: str, result_hash: str) -> dict:
        """POST /purchase/{id}/result — submit cryptographic hash of delivered data."""
        payload = {"result_hash": result_hash}
        resp = await self._client.post(
            f"/purchase/{escrow_id}/result", json=payload
        )
        resp.raise_for_status()
        return resp.json()

    async def request_refund(self, escrow_id: str, reason: str) -> dict:
        """POST /purchase/{id}/request-refund — trigger automated refund."""
        payload = {"reason": reason}
        resp = await self._client.post(
            f"/purchase/{escrow_id}/request-refund", json=payload
        )
        resp.raise_for_status()
        return resp.json()

    async def get_decision_log(self, escrow_id: str) -> list[dict]:
        """GET /purchase/{id}/log — immutable decision logging (Masumi registry)."""
        resp = await self._client.get(f"/purchase/{escrow_id}/log")
        resp.raise_for_status()
        return resp.json()

    async def x402_pay_for_data(
        self,
        amount_lovelace: int,
        data_description: str,
        data_callback: callable,  # async callable
    ) -> dict:
        """Full x402 lifecycle: lock -> fetch -> submit -> complete.

        amount_lovelace: payment in lovelace (1 ADA = 1_000_000 lovelace)
        data_description: metadata describing what is being paid for
        data_callback: async function that fetches the data once payment is locked
        """
        escrow = await self.create_escrow(
            amount_lovelace=amount_lovelace,
            metadata={"description": data_description},
        )
        escrow_id = escrow.get("id") or escrow.get("purchase_id")
        if not escrow_id:
            raise ValueError(f"No escrow ID in response: {escrow}")

        status = await self.check_escrow_status(escrow_id)
        if status != EscrowState.funds_locked:
            raise RuntimeError(
                f"Escrow {escrow_id} in state {status}, expected FundsLocked"
            )

        result_data = await data_callback()
        result_hash = self._hash_result(result_data)
        await self.submit_result(escrow_id, result_hash)

        final_status = await self.check_escrow_status(escrow_id)
        return {
            "escrow_id": escrow_id,
            "final_state": final_status.value,
            "result_data": result_data,
        }

    @staticmethod
    def _hash_result(data: dict) -> str:
        import hashlib
        serialised = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(serialised.encode()).hexdigest()
