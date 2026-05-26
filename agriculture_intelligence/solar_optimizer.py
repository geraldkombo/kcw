"""Solar optimizer — leverages equatorial solar radiation for maximum agricultural value.
Kenya receives 4-8 kWh/m2/day year-round (vs Europe's 1-3). This module quantifies
that advantage for crop selection, solar irrigation, and solar drying."""

from satellite.power_client import PowerClient


class SolarOptimizer:
    """Quantifies and optimises the equatorial solar advantage for agriculture."""

    def __init__(self, power: PowerClient | None = None):
        self.power = power or PowerClient()

    async def get_solar_advantage(self, latitude: float, longitude: float) -> dict:
        """Compute the equatorial solar advantage for this location."""
        solar = await self.power.get_solar_radiation(latitude, longitude)
        temp = await self.power.get_temperature(latitude, longitude)

        # Comparison benchmarks
        europe_avg = 2.5  # kWh/m2/day
        kenya_avg = 5.5
        advantage_vs_europe = round(min(200, (solar - europe_avg) / europe_avg * 100), 1)

        # Solar energy potential
        solar_kwh_per_ha_per_day = solar * 10000  # 1 ha = 10,000 m2
        solar_kwh_per_ha_per_year = solar_kwh_per_ha_per_day * 365

        # Crop yield boost from solar (simplified model)
        # More solar = more photosynthesis, up to a point
        photosynthetically_active = solar * 0.48  # PAR is ~48% of total solar
        yield_boost_vs_europe = min(100, round((solar - 2.5) / 2.5 * 60, 1))

        return {
            "latitude": latitude,
            "longitude": longitude,
            "current_solar_kwh_m2_day": round(solar, 2),
            "equatorial_advantage_pct": advantage_vs_europe,
            "solar_kwh_per_ha_per_day": round(solar_kwh_per_ha_per_day),
            "solar_kwh_per_ha_per_year": round(solar_kwh_per_ha_per_year),
            "yield_boost_vs_temperate_pct": yield_boost_vs_europe,
            "solar_drying_potential": "excellent" if solar > 5.0 else "good" if solar > 3.5 else "moderate",
            "solar_irrigation_payback_years": round(80000 / (solar * 365 * 0.5), 1) if solar > 0 else 0,
            "recommendation": (
                f"At {solar:.1f} kWh/m2/day, this location has {advantage_vs_europe}% more solar radiation "
                f"than temperate agriculture. Solar-powered irrigation has strong ROI. High-value sun-loving "
                f"crops (sunflower, maize, drought-resistant seed) will outperform shade-tolerant crops (tea, coffee)."
            ),
        }

    async def get_crop_solar_classification(self) -> list[dict]:
        """Classify crops by solar requirement for equatorial optimization."""
        return [
            {"crop": "Sunflower", "solar_need": "high", "optimal_kwh_m2_day": "5-9", "equatorial_advantage": "maximal"},
            {"crop": "Drought Resistant Seed", "solar_need": "high", "optimal_kwh_m2_day": "5-10", "equatorial_advantage": "maximal"},
            {"crop": "Maize", "solar_need": "medium-high", "optimal_kwh_m2_day": "4-8", "equatorial_advantage": "strong"},
            {"crop": "Beans", "solar_need": "medium", "optimal_kwh_m2_day": "3-6", "equatorial_advantage": "moderate"},
            {"crop": "Wheat", "solar_need": "medium", "optimal_kwh_m2_day": "4-7", "equatorial_advantage": "moderate"},
            {"crop": "Coffee", "solar_need": "medium-low", "optimal_kwh_m2_day": "3-6", "equatorial_advantage": "moderate"},
            {"crop": "Tea", "solar_need": "low-medium", "optimal_kwh_m2_day": "3-6", "equatorial_advantage": "limited"},
        ]

    async def get_solar_drying_feasibility(self, latitude: float, longitude: float, crop: str = "maize") -> dict:
        """Assess solar drying potential for post-harvest processing."""
        solar = await self.power.get_solar_radiation(latitude, longitude)
        temp = await self.power.get_temperature(latitude, longitude)
        precip = await self.power.get_precipitation(latitude, longitude)

        drying_days = 0
        if solar > 4.0 and precip < 3.0:
            drying_days = 3
        elif solar > 3.0 and precip < 5.0:
            drying_days = 5
        else:
            drying_days = 7

        moisture_content_reduction = min(25, round(solar * 3))  # percentage points

        return {
            "crop": crop,
            "solar_kwh_m2_day": round(solar, 2),
            "temp_c": round(temp.get("mean", 25), 1),
            "estimated_drying_days": drying_days,
            "moisture_reduction_pct": moisture_content_reduction,
            "solar_drier_recommended": solar > 4.0,
            "post_harvest_loss_saved_pct": round(solar * 6, 1),
            "recommendation": (
                f"Solar drying feasible in {drying_days} days. "
                f"Could save {round(solar * 6, 1)}% of post-harvest losses using solar driers."
                if solar > 4.0
                else "Solar drying marginal; consider mechanical drying."
            ),
        }
