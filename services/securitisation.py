import uuid
import math
from datetime import datetime
from typing import Optional

from models.pool import SecuritisationPool, PoolStatus


class SecuritisationService:
    """Manages securitisation pool assembly, expected revenue calculation,
    and tranche structuring.

    Expected revenue formula:
    E = sum_{i=1}^{N} A_i * (1 + r_i) * (1 - PD_i)
    """

    def __init__(self):
        self._pools: dict[str, SecuritisationPool] = {}

    def build_pool(self, farmer_data: list[dict]) -> SecuritisationPool:
        pool_id = f"POOL-{uuid.uuid4().hex[:8].upper()}"
        loans = [f for f in farmer_data if f.get("probability_default", 1) < 0.35]

        total_notional = sum(
            f.get("max_loan_kes", 0) or f.get("amount_kes", 0) for f in loans
        )
        if not loans:
            return SecuritisationPool(
                id=pool_id,
                name=f"Empty Pool {pool_id}",
                status=PoolStatus.assembling,
            )

        avg_pd = sum(f.get("probability_default", 0) for f in loans) / len(loans)

        # E = sum A_i * (1 + r_i) * (1 - PD_i)
        expected_revenue = 0.0
        for f in loans:
            A = f.get("max_loan_kes", 0) or f.get("amount_kes", 0)
            r = f.get("interest_rate_annual", 18.0) / 100
            pd = f.get("probability_default", 0.1)
            expected_revenue += A * (1 + r) * (1 - pd)

        pool = SecuritisationPool(
            id=pool_id,
            name=f"KCW Pool {pool_id} ({len(loans)} farmers)",
            status=PoolStatus.assembling,
            loan_ids=[f.get("loan_id", "") for f in loans if f.get("loan_id")],
            total_notional_kes=round(total_notional, 2),
            farmer_count=len(loans),
            avg_pd=round(avg_pd, 4),
            expected_revenue_kes=round(expected_revenue, 2),
            target_rating=self._infer_rating(avg_pd),
        )
        self._pools[pool_id] = pool
        return pool

    def get_pool(self, pool_id: str) -> Optional[dict]:
        pool = self._pools.get(pool_id)
        return pool.model_dump() if pool else None

    def list_pools(self) -> list[dict]:
        return [p.model_dump() for p in self._pools.values()]

    def _infer_rating(self, avg_pd: float) -> str:
        if avg_pd < 0.05:
            return "A"
        elif avg_pd < 0.10:
            return "BBB+"
        elif avg_pd < 0.15:
            return "BBB"
        elif avg_pd < 0.20:
            return "BBB-"
        elif avg_pd < 0.30:
            return "BB"
        else:
            return "B"
