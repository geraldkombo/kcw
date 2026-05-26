from datetime import datetime
from typing import Optional

from services.securitisation import SecuritisationService


class LiquidityAgent:
    """Liquidity Pooling Agent — assembles securitisation pools,
    computes expected revenue E, and manages tranche structure.
    """

    def __init__(
        self, securitisation: Optional[SecuritisationService] = None
    ):
        self.securitisation = securitisation or SecuritisationService()

    async def assemble_pool(self, farmer_data: list[dict]) -> dict:
        pool = self.securitisation.build_pool(farmer_data)
        return pool.model_dump()

    async def get_pool_summary(self, pool_id: str) -> dict:
        return self.securitisation.get_pool(pool_id)

    async def list_pools(self) -> list[dict]:
        return self.securitisation.list_pools()
