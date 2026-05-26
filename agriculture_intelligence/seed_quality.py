"""Seed quality analyzer — predicts germination rates, identifies poor-quality seed,
and recommends optimal seed varieties based on local conditions."""

from satellite.power_client import PowerClient


class SeedQualityAnalyzer:
    """Analyses seed quality, predicts germination rates, and recommends seed varieties."""

    SEED_VARIETIES = {
        "maize": {
            "droughtguard_301": {"germination_rate": 0.92, "days_to_maturity": 110, "drought_tolerance": "high", "yield_tonnes_ha": 3.5, "cost_kes_per_kg": 450},
            "hybrid_525": {"germination_rate": 0.88, "days_to_maturity": 130, "drought_tolerance": "medium", "yield_tonnes_ha": 4.0, "cost_kes_per_kg": 380},
            "local_landrace": {"germination_rate": 0.75, "days_to_maturity": 150, "drought_tolerance": "low", "yield_tonnes_ha": 1.8, "cost_kes_per_kg": 120},
        },
        "beans": {
            "droughtguard_101": {"germination_rate": 0.90, "days_to_maturity": 75, "drought_tolerance": "high", "yield_tonnes_ha": 1.8, "cost_kes_per_kg": 350},
            "rosecoco": {"germination_rate": 0.82, "days_to_maturity": 90, "drought_tolerance": "medium", "yield_tonnes_ha": 1.4, "cost_kes_per_kg": 280},
            "mwezi_moja": {"germination_rate": 0.85, "days_to_maturity": 85, "drought_tolerance": "medium", "yield_tonnes_ha": 1.5, "cost_kes_per_kg": 300},
        },
    }

    def __init__(self, power: PowerClient | None = None):
        self.power = power or PowerClient()

    async def predict_germination(self, crop: str, variety: str, latitude: float, longitude: float) -> dict:
        """Predict actual germination rate adjusted for local conditions."""
        crop_varieties = self.SEED_VARIETIES.get(crop, {})
        seed = crop_varieties.get(variety)
        if not seed:
            return {"error": f"Unknown variety {variety} for {crop}"}

        temp = await self.power.get_temperature(latitude, longitude)
        solar = await self.power.get_solar_radiation(latitude, longitude)
        precip = await self.power.get_precipitation(latitude, longitude)

        # Germination adjustment based on conditions
        t_mean = temp.get("mean", 25)
        adjustment = 1.0
        if 18 <= t_mean <= 30:
            adjustment *= 1.05  # Optimal temp
        elif t_mean > 35 or t_mean < 12:
            adjustment *= 0.7  # Stress

        if precip > 3.0 and precip < 10.0:
            adjustment *= 1.03
        elif precip < 1.0:
            adjustment *= 0.8

        # Avoid unrealistic germination
        adjusted_rate = min(0.98, seed["germination_rate"] * adjustment)

        # Calculate losses from poor germination
        loss_percentage = (seed["germination_rate"] - adjusted_rate) * 100
        financial_loss_per_kg = seed["cost_kes_per_kg"] * (1 - adjusted_rate / seed["germination_rate"])

        return {
            "crop": crop,
            "variety": variety,
            "base_germination_rate": seed["germination_rate"],
            "adjusted_germination_rate": round(adjusted_rate, 3),
            "adjustment_factor": round(adjustment, 3),
            "loss_due_to_conditions_pct": round(max(0, loss_percentage), 1),
            "financial_loss_kes_per_kg": round(financial_loss_per_kg),
            "local_temp_c": t_mean,
            "local_precip_mm_day": precip,
            "local_solar_kwh_m2_day": solar,
        }

    async def recommend_best_seed(self, crop: str, latitude: float, longitude: float, budget_kes: float = 5000) -> dict:
        """Recommend the best seed variety for local conditions and budget."""
        crop_varieties = self.SEED_VARIETIES.get(crop, {})
        if not crop_varieties:
            return {"error": f"No seed data for {crop}"}

        temp = await self.power.get_temperature(latitude, longitude)
        precip = await self.power.get_precipitation(latitude, longitude)
        drought_risk_val = 0.3
        if precip < 2.5:
            drought_risk_val = 0.6

        results = []
        for variety, data in crop_varieties.items():
            seed_per_ha = 25 if crop == "maize" else 60  # kg/ha
            cost_per_ha = seed_per_ha * data["cost_kes_per_kg"]

            # Score variety
            drought_score = 1.0 if data["drought_tolerance"] == "high" else 0.6 if data["drought_tolerance"] == "medium" else 0.3
            suitability = 0.4 * data["germination_rate"] + 0.3 * drought_score + 0.3 * (1 - drought_risk_val)
            revenue = data["yield_tonnes_ha"] * 45000  # maize price KES/tonne
            profit = revenue - cost_per_ha

            results.append({
                "variety": variety,
                "germination_rate": data["germination_rate"],
                "drought_tolerance": data["drought_tolerance"],
                "yield_tonnes_ha": data["yield_tonnes_ha"],
                "cost_kes_per_kg": data["cost_kes_per_kg"],
                "cost_kes_per_ha": round(cost_per_ha),
                "suitability_score": round(suitability, 3),
                "estimated_revenue_kes_ha": round(revenue),
                "estimated_profit_kes_ha": round(profit),
                "roi_percent": round((profit - cost_per_ha) / cost_per_ha * 100, 1),
            })

        results.sort(key=lambda r: r["suitability_score"], reverse=True)

        best = results[0]
        return {
            "crop": crop,
            "recommended_variety": best["variety"],
            "reason": f"Best germination ({best['germination_rate']*100:.0f}%), highest suitability ({best['suitability_score']:.2f}), est. profit KES {best['estimated_profit_kes_ha']:,}/ha",
            "alternatives": results[1:],
            "all_options": results,
            "local_drought_risk": drought_risk_val,
        }
