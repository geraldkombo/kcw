"""Sprout API client — Mercy Corps AgriFin open content platform.
Sprout is migrating from DKAN to CKAN (March 2026+) and will expose
a public REST/GraphQL API for agricultural advisory content retrieval.

Current status: CKAN migration in progress. Client implemented as a
future-ready stub with the expected CKAN API pattern.
Docs: https://www.sproutopencontent.com/
"""

from typing import Any

import httpx


class SproutClient:
    """Client for the Sprout open content platform (CKAN-based).

    Once the CKAN migration is complete, this client can retrieve
    farmer-friendly advisory content — agronomy tips, weather advisories,
    market prices, pest alerts — and inject them into the KCW agent pipeline.
    """

    def __init__(self, base_url: str = "", api_key: str | None = None):
        self.base_url = base_url or "https://sproutopencontent.com/api"
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))

    async def search_content(
        self,
        query: str,
        page: int = 1,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search Sprout content by keyword (CKAN package_search pattern).

        Once live, this will return datasets of farmer-facing advisory
        content filtered by crop type, county, language, and value chain.
        """
        params = {
            "q": query,
            "rows": limit,
            "start": (page - 1) * limit,
        }
        headers = {}
        if self.api_key:
            headers["Authorization"] = self.api_key

        try:
            resp = await self._client.get(
                f"{self.base_url}/3/action/package_search",
                params=params,
                headers=headers,
            )
            resp.raise_for_status()
            result = resp.json()
            return result.get("result", {}).get("results", [])
        except Exception:
            return []

    async def get_content_by_county(self, county: str) -> list[dict[str, Any]]:
        """Get advisory content specific to a Kenyan county."""
        return await self.search_content(f"county:{county}")

    async def get_farmer_advisory(self, farmer_profile: dict) -> dict | None:
        """Get a relevant advisory for a specific farmer profile."""
        query_parts = []
        if farmer_profile.get("county"):
            query_parts.append(farmer_profile["county"])
        if farmer_profile.get("primary_crop"):
            query_parts.append(farmer_profile["primary_crop"])
        query = " ".join(query_parts)

        results = await self.search_content(query, limit=1)
        if results:
            return {
                "title": results[0].get("title", ""),
                "notes": results[0].get("notes", ""),
                "source": "sprout",
            }
        return None

    async def close(self):
        await self._client.aclose()
