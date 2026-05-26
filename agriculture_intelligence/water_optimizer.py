"""Water optimizer — precision irrigation scheduling from NASA POWER real-time data.
Derisks water use by telling farmers exactly when and how much to irrigate."""

from satellite.power_client import PowerClient


class WaterOptimizer:
    """Optimises irrigation scheduling using real NASA POWER satellite data.
    Computes water deficit, recommends irrigation volume, and projects savings."""

    SOIL_TYPES = {
        "sandy": {"field_capacity": 0.15, "wilting_point": 0.05, "infiltration_rate": 30},
        "loamy": {"field_capacity": 0.35, "wilting_point": 0.12, "infiltration_rate": 15},
        "clay": {"field_capacity": 0.50, "wilting_point": 0.25, "infiltration_rate": 5},
    }

    def __init__(self, power: PowerClient | None = None):
        self.power = power or PowerClient()

    async def compute_water_deficit(
        self, latitude: float, longitude: float, crop: str = "maize",
        soil_type: str = "loamy", farm_size_ha: float = 1.0,
    ) -> dict:
        """Compute current water deficit and irrigation recommendation."""
        temp = await self.power.get_temperature(latitude, longitude)
        precip = await self.power.get_precipitation(latitude, longitude)
        solar = await self.power.get_solar_radiation(latitude, longitude)

        props = await self.power.get_ag_point(latitude, longitude)
        gwetroot = self.power._extract_mean(props, "GWETROOT") or 0.3

        soil = self.SOIL_TYPES.get(soil_type, self.SOIL_TYPES["loamy"])
        # Current soil moisture as fraction of field capacity
        current_moisture_frac = min(1.0, gwetroot / soil["field_capacity"])
        deficit_fraction = 1.0 - current_moisture_frac

        # Evapotranspiration estimate (simplified Hargreaves)
        t_mean = temp.get("mean", 25.0)
        et0_mm_day = max(0.1, 0.0023 * solar * (t_mean + 17.8))  # Hargreaves-Samani

        # Crop coefficient (simplified by growth stage)
        kc = 1.0
        etc_mm_day = et0_mm_day * kc  # Crop evapotranspiration

        # Water balance
        effective_rainfall = precip * 0.8  # 80% efficiency
        net_irrigation_need = max(0, etc_mm_day - effective_rainfall)
        irrigation_volume_m3_per_ha = net_irrigation_need * 10  # 1 mm = 10 m3/ha

        total_volume_m3 = irrigation_volume_m3_per_ha * farm_size_ha
        water_cost_kes = total_volume_m3 * 30  # ~KES 30/m3 (pumping + distribution)

        # Annual projection
        dry_months = 4  # Typical Kenyan dry season months
        annual_irrigation_volume = irrigation_volume_m3_per_ha * 30 * dry_months
        annual_irrigation_cost = annual_irrigation_volume * farm_size_ha * 30

        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "crop": crop,
            "soil_type": soil_type,
            "farm_size_ha": farm_size_ha,
            "current_moisture_fraction": round(current_moisture_frac, 2),
            "deficit_fraction": round(deficit_fraction, 2),
            "et0_mm_day": round(et0_mm_day, 2),
            "etc_mm_day": round(etc_mm_day, 2),
            "effective_rainfall_mm_day": round(effective_rainfall, 2),
            "daily_irrigation_need_mm": round(net_irrigation_need, 2),
            "daily_irrigation_volume_m3_ha": round(irrigation_volume_m3_per_ha, 1),
            "total_daily_volume_m3": round(total_volume_m3, 1),
            "daily_water_cost_kes": round(water_cost_kes),
            "annual_irrigation_volume_m3": round(annual_irrigation_volume),
            "annual_irrigation_cost_kes": round(annual_irrigation_cost),
            "recommendation": (
                f"Irrigate {net_irrigation_need:.1f}mm/day ({total_volume_m3:.1f}m3 total). "
                f"Estimated cost: KES {water_cost_kes}/day. "
                f"Yield gain from irrigation: estimated 40-60% vs rainfed."
                if net_irrigation_need > 0.5
                else "No irrigation needed — natural rainfall is sufficient."
            ),
            "solar_irrigation_feasible": solar > 4.0,
        }

    async def get_conservation_plan(self, latitude: float, longitude: float) -> dict:
        """Generate water conservation recommendations based on climate data."""
        temp = await self.power.get_temperature(latitude, longitude)
        precip = await self.power.get_precipitation(latitude, longitude)
        solar = await self.power.get_solar_radiation(latitude, longitude)

        strategies = []
        if solar > 6.0:
            strategies.append({
                "strategy": "Solar-powered drip irrigation",
                "savings_pct": 60,
                "cost_kes_per_ha": 120000,
                "payback_months": 18,
                "detail": "Equatorial solar ({} kW-hr/m2/day) makes solar pumping viable. Drip reduces water use 60% vs flood.".format(round(solar, 1)),
            })
        if precip < 3.0:
            strategies.append({
                "strategy": "Rainwater harvesting",
                "savings_pct": 30,
                "cost_kes_per_ha": 50000,
                "payback_months": 12,
                "detail": "At {:.1f}mm/day, capture and store roof/runoff water for dry spells.".format(precip),
            })
        if temp.get("mean", 25) > 28:
            strategies.append({
                "strategy": "Mulching & shade nets",
                "savings_pct": 25,
                "cost_kes_per_ha": 30000,
                "payback_months": 6,
                "detail": "Reduces soil evaporation by 25% in high-heat conditions ({:.1f}C).".format(temp.get("mean")),
            })

        return {
            "location": {"latitude": latitude, "longitude": longitude},
            "conservation_strategies": strategies,
            "best_strategy": strategies[0] if strategies else None,
            "total_potential_savings_pct": sum(s["savings_pct"] for s in strategies),
        }
