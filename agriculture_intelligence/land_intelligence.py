"""Land intelligence — suitability analysis, idle land detection, soil health scoring,
yield prediction, and contract-farm matching using NASA POWER satellite data."""

from satellite.power_client import PowerClient


class LandIntelligence:
    """Analyses agricultural land for suitability, soil health, idle status, and yield potential."""

    # Crop-specific growing requirements (optimal ranges)
    CROP_REQUIREMENTS = {
        "maize": {
            "temp_min": 18, "temp_max": 32, "temp_opt": 25,
            "precip_min": 3.0, "precip_max": 8.0, "precip_opt": 5.0,
            "solar_min": 4.0, "solar_max": 8.0,
            "soil_moisture_min": 0.3, "soil_moisture_opt": 0.6,
            "growing_days": 120, "water_need_mm_total": 500,
        },
        "beans": {
            "temp_min": 15, "temp_max": 28, "temp_opt": 22,
            "precip_min": 3.0, "precip_max": 6.0, "precip_opt": 4.0,
            "solar_min": 3.0, "solar_max": 6.0,
            "soil_moisture_min": 0.35, "soil_moisture_opt": 0.55,
            "growing_days": 90, "water_need_mm_total": 350,
        },
        "tea": {
            "temp_min": 15, "temp_max": 28, "temp_opt": 22,
            "precip_min": 4.0, "precip_max": 12.0, "precip_opt": 7.0,
            "solar_min": 3.0, "solar_max": 6.0,
            "soil_moisture_min": 0.5, "soil_moisture_opt": 0.7,
            "growing_days": 365, "water_need_mm_total": 1200,
        },
        "coffee": {
            "temp_min": 15, "temp_max": 28, "temp_opt": 22,
            "precip_min": 4.0, "precip_max": 10.0, "precip_opt": 6.0,
            "solar_min": 3.0, "solar_max": 6.0,
            "soil_moisture_min": 0.4, "soil_moisture_opt": 0.65,
            "growing_days": 240, "water_need_mm_total": 800,
        },
        "wheat": {
            "temp_min": 10, "temp_max": 25, "temp_opt": 18,
            "precip_min": 2.5, "precip_max": 5.0, "precip_opt": 3.5,
            "solar_min": 4.0, "solar_max": 7.0,
            "soil_moisture_min": 0.3, "soil_moisture_opt": 0.55,
            "growing_days": 150, "water_need_mm_total": 450,
        },
        "sunflower": {
            "temp_min": 18, "temp_max": 35, "temp_opt": 26,
            "precip_min": 2.0, "precip_max": 5.0, "precip_opt": 3.0,
            "solar_min": 5.0, "solar_max": 9.0,
            "soil_moisture_min": 0.2, "soil_moisture_opt": 0.4,
            "growing_days": 120, "water_need_mm_total": 350,
        },
        "drought_resistant_seed": {
            "temp_min": 20, "temp_max": 38, "temp_opt": 28,
            "precip_min": 1.0, "precip_max": 4.0, "precip_opt": 2.0,
            "solar_min": 5.0, "solar_max": 10.0,
            "soil_moisture_min": 0.1, "soil_moisture_opt": 0.3,
            "growing_days": 90, "water_need_mm_total": 200,
        },
        # Indigenous / traditional food plants (Maundu et al., 1999)
        "amaranth": {
            "temp_min": 18, "temp_max": 32, "temp_opt": 24,
            "precip_min": 2.0, "precip_max": 6.0, "precip_opt": 3.5,
            "solar_min": 3.0, "solar_max": 8.0,
            "soil_moisture_min": 0.2, "soil_moisture_opt": 0.4,
            "growing_days": 45, "water_need_mm_total": 200,
        },
        "black_nightshade": {
            "temp_min": 16, "temp_max": 28, "temp_opt": 22,
            "precip_min": 3.0, "precip_max": 6.0, "precip_opt": 4.0,
            "solar_min": 3.0, "solar_max": 6.0,
            "soil_moisture_min": 0.3, "soil_moisture_opt": 0.5,
            "growing_days": 35, "water_need_mm_total": 160,
        },
        "spider_plant": {
            "temp_min": 18, "temp_max": 30, "temp_opt": 24,
            "precip_min": 2.5, "precip_max": 5.5, "precip_opt": 3.5,
            "solar_min": 3.0, "solar_max": 7.0,
            "soil_moisture_min": 0.25, "soil_moisture_opt": 0.45,
            "growing_days": 40, "water_need_mm_total": 180,
        },
        "cowpea_leaves": {
            "temp_min": 18, "temp_max": 35, "temp_opt": 26,
            "precip_min": 1.5, "precip_max": 5.0, "precip_opt": 3.0,
            "solar_min": 4.0, "solar_max": 9.0,
            "soil_moisture_min": 0.15, "soil_moisture_opt": 0.35,
            "growing_days": 60, "water_need_mm_total": 250,
        },
        "jute_mallow": {
            "temp_min": 20, "temp_max": 35, "temp_opt": 28,
            "precip_min": 2.5, "precip_max": 6.0, "precip_opt": 4.0,
            "solar_min": 4.0, "solar_max": 8.0,
            "soil_moisture_min": 0.25, "soil_moisture_opt": 0.5,
            "growing_days": 40, "water_need_mm_total": 200,
        },
        "pumpkin_leaves": {
            "temp_min": 18, "temp_max": 32, "temp_opt": 25,
            "precip_min": 2.0, "precip_max": 5.5, "precip_opt": 3.5,
            "solar_min": 4.0, "solar_max": 8.0,
            "soil_moisture_min": 0.2, "soil_moisture_opt": 0.4,
            "growing_days": 60, "water_need_mm_total": 250,
        },
        "sorghum": {
            "temp_min": 20, "temp_max": 38, "temp_opt": 28,
            "precip_min": 1.5, "precip_max": 5.0, "precip_opt": 3.0,
            "solar_min": 5.0, "solar_max": 10.0,
            "soil_moisture_min": 0.1, "soil_moisture_opt": 0.3,
            "growing_days": 120, "water_need_mm_total": 350,
        },
        "finger_millet": {
            "temp_min": 18, "temp_max": 30, "temp_opt": 24,
            "precip_min": 2.5, "precip_max": 6.0, "precip_opt": 4.0,
            "solar_min": 4.0, "solar_max": 8.0,
            "soil_moisture_min": 0.2, "soil_moisture_opt": 0.4,
            "growing_days": 120, "water_need_mm_total": 350,
        },
        "pigeon_pea": {
            "temp_min": 18, "temp_max": 35, "temp_opt": 26,
            "precip_min": 1.5, "precip_max": 5.0, "precip_opt": 3.0,
            "solar_min": 5.0, "solar_max": 9.0,
            "soil_moisture_min": 0.1, "soil_moisture_opt": 0.3,
            "growing_days": 150, "water_need_mm_total": 400,
        },
        "bambara_nut": {
            "temp_min": 20, "temp_max": 35, "temp_opt": 28,
            "precip_min": 2.0, "precip_max": 5.0, "precip_opt": 3.0,
            "solar_min": 5.0, "solar_max": 9.0,
            "soil_moisture_min": 0.15, "soil_moisture_opt": 0.3,
            "growing_days": 130, "water_need_mm_total": 350,
        },
        "sweet_potato": {
            "temp_min": 15, "temp_max": 30, "temp_opt": 22,
            "precip_min": 2.5, "precip_max": 6.0, "precip_opt": 4.0,
            "solar_min": 3.0, "solar_max": 7.0,
            "soil_moisture_min": 0.2, "soil_moisture_opt": 0.4,
            "growing_days": 120, "water_need_mm_total": 350,
        },
        "cassava": {
            "temp_min": 18, "temp_max": 35, "temp_opt": 26,
            "precip_min": 2.0, "precip_max": 7.0, "precip_opt": 4.5,
            "solar_min": 4.0, "solar_max": 9.0,
            "soil_moisture_min": 0.15, "soil_moisture_opt": 0.35,
            "growing_days": 300, "water_need_mm_total": 800,
        },
        "yam": {
            "temp_min": 20, "temp_max": 34, "temp_opt": 27,
            "precip_min": 3.0, "precip_max": 7.0, "precip_opt": 5.0,
            "solar_min": 3.0, "solar_max": 6.0,
            "soil_moisture_min": 0.3, "soil_moisture_opt": 0.5,
            "growing_days": 240, "water_need_mm_total": 700,
        },
        "baobab": {
            "temp_min": 20, "temp_max": 40, "temp_opt": 30,
            "precip_min": 1.0, "precip_max": 4.0, "precip_opt": 2.0,
            "solar_min": 6.0, "solar_max": 11.0,
            "soil_moisture_min": 0.05, "soil_moisture_opt": 0.15,
            "growing_days": 365, "water_need_mm_total": 500,
        },
        "tamarind": {
            "temp_min": 22, "temp_max": 40, "temp_opt": 30,
            "precip_min": 1.0, "precip_max": 4.0, "precip_opt": 2.0,
            "solar_min": 6.0, "solar_max": 11.0,
            "soil_moisture_min": 0.05, "soil_moisture_opt": 0.15,
            "growing_days": 365, "water_need_mm_total": 400,
        },
        # Ojwang (2020) — Homa Bay traditional vegetables
        "dek": {
            "temp_min": 18, "temp_max": 32, "temp_opt": 24,
            "precip_min": 2.5, "precip_max": 6.0, "precip_opt": 4.0,
            "solar_min": 3.0, "solar_max": 7.0,
            "soil_moisture_min": 0.2, "soil_moisture_opt": 0.4,
            "growing_days": 35, "water_need_mm_total": 180,
        },
        "mito": {
            "temp_min": 18, "temp_max": 30, "temp_opt": 24,
            "precip_min": 2.5, "precip_max": 5.5, "precip_opt": 3.5,
            "solar_min": 3.0, "solar_max": 7.0,
            "soil_moisture_min": 0.25, "soil_moisture_opt": 0.45,
            "growing_days": 40, "water_need_mm_total": 200,
        },
        "boo": {
            "temp_min": 16, "temp_max": 30, "temp_opt": 23,
            "precip_min": 2.0, "precip_max": 5.5, "precip_opt": 3.5,
            "solar_min": 3.0, "solar_max": 7.0,
            "soil_moisture_min": 0.2, "soil_moisture_opt": 0.4,
            "growing_days": 45, "water_need_mm_total": 220,
        },
        "atipa": {
            "temp_min": 18, "temp_max": 32, "temp_opt": 25,
            "precip_min": 3.0, "precip_max": 6.0, "precip_opt": 4.5,
            "solar_min": 3.0, "solar_max": 7.0,
            "soil_moisture_min": 0.25, "soil_moisture_opt": 0.5,
            "growing_days": 30, "water_need_mm_total": 160,
        },
        "odielo": {
            "temp_min": 18, "temp_max": 32, "temp_opt": 24,
            "precip_min": 2.5, "precip_max": 6.0, "precip_opt": 4.0,
            "solar_min": 3.0, "solar_max": 7.0,
            "soil_moisture_min": 0.2, "soil_moisture_opt": 0.4,
            "growing_days": 35, "water_need_mm_total": 180,
        },
        "ndemra": {
            "temp_min": 16, "temp_max": 34, "temp_opt": 25,
            "precip_min": 2.0, "precip_max": 5.5, "precip_opt": 3.5,
            "solar_min": 4.0, "solar_max": 8.0,
            "soil_moisture_min": 0.15, "soil_moisture_opt": 0.35,
            "growing_days": 40, "water_need_mm_total": 200,
        },
        "alikra": {
            "temp_min": 18, "temp_max": 32, "temp_opt": 24,
            "precip_min": 2.5, "precip_max": 6.0, "precip_opt": 4.0,
            "solar_min": 3.0, "solar_max": 7.0,
            "soil_moisture_min": 0.2, "soil_moisture_opt": 0.4,
            "growing_days": 35, "water_need_mm_total": 180,
        },
        "ng_or": {
            "temp_min": 18, "temp_max": 34, "temp_opt": 26,
            "precip_min": 2.0, "precip_max": 5.5, "precip_opt": 3.5,
            "solar_min": 4.0, "solar_max": 8.0,
            "soil_moisture_min": 0.15, "soil_moisture_opt": 0.35,
            "growing_days": 110, "water_need_mm_total": 350,
        },
        "mapera": {
            "temp_min": 18, "temp_max": 35, "temp_opt": 26,
            "precip_min": 2.0, "precip_max": 6.0, "precip_opt": 4.0,
            "solar_min": 4.0, "solar_max": 9.0,
            "soil_moisture_min": 0.15, "soil_moisture_opt": 0.35,
            "growing_days": 240, "water_need_mm_total": 600,
        },
        "slenderleaf": {
            "temp_min": 16, "temp_max": 30, "temp_opt": 23,
            "precip_min": 2.5, "precip_max": 6.0, "precip_opt": 4.0,
            "solar_min": 3.0, "solar_max": 7.0,
            "soil_moisture_min": 0.2, "soil_moisture_opt": 0.4,
            "growing_days": 60, "water_need_mm_total": 250,
        },
        "desert_date": {
            "temp_min": 24, "temp_max": 42, "temp_opt": 32,
            "precip_min": 0.5, "precip_max": 3.0, "precip_opt": 1.5,
            "solar_min": 7.0, "solar_max": 12.0,
            "soil_moisture_min": 0.05, "soil_moisture_opt": 0.15,
            "growing_days": 365, "water_need_mm_total": 300,
        },
        "bird_plum": {
            "temp_min": 22, "temp_max": 40, "temp_opt": 30,
            "precip_min": 0.5, "precip_max": 3.0, "precip_opt": 1.5,
            "solar_min": 6.0, "solar_max": 11.0,
            "soil_moisture_min": 0.05, "soil_moisture_opt": 0.15,
            "growing_days": 365, "water_need_mm_total": 300,
        },
        "vitex_black_plum": {
            "temp_min": 20, "temp_max": 34, "temp_opt": 26,
            "precip_min": 2.0, "precip_max": 5.5, "precip_opt": 3.5,
            "solar_min": 4.0, "solar_max": 8.0,
            "soil_moisture_min": 0.15, "soil_moisture_opt": 0.35,
            "growing_days": 240, "water_need_mm_total": 600,
        },
    }

    SOIL_HEALTH_INDICATORS = {
        "good": {"description": "Adequate moisture and moderate temperature — suitable for most crops", "irrigation_needed": False},
        "moderate": {"description": "Marginal moisture or temperature stress — irrigation recommended", "irrigation_needed": True},
        "poor": {"description": "Low moisture or extreme temperature — requires drought-resistant varieties or irrigation infrastructure", "irrigation_needed": True},
    }

    def __init__(self, power: PowerClient | None = None):
        self.power = power or PowerClient()

    async def analyse_land_suitability(self, latitude: float, longitude: float, county: str, farm_size_ha: float) -> dict:
        """Determine what crops are suitable for this specific land based on real satellite data."""
        temp = await self.power.get_temperature(latitude, longitude)
        precip = await self.power.get_precipitation(latitude, longitude)
        solar = await self.power.get_solar_radiation(latitude, longitude)
        moisture_stress = await self.power.get_moisture_stress(latitude, longitude)
        soil_quality = await self.power.get_soil_quality(latitude, longitude)

        gwetroot_val = None
        try:
            props = await self.power.get_ag_point(latitude, longitude)
            gwetroot_val = self.power._extract_mean(props, "GWETROOT")
        except Exception:
            pass

        results = []
        for crop, req in self.CROP_REQUIREMENTS.items():
            temp_ok = req["temp_min"] <= temp.get("mean", 25) <= req["temp_max"]
            precip_ok = req["precip_min"] <= precip <= req["precip_max"]
            solar_ok = req["solar_min"] <= solar <= req["solar_max"]
            moisture_ok = True
            if gwetroot_val is not None:
                moisture_ok = gwetroot_val >= req["soil_moisture_min"]

            score = sum([temp_ok, precip_ok, solar_ok, moisture_ok]) / 4.0

            # Irrigation gap: how much water is needed beyond natural rainfall
            growing_days = req["growing_days"]
            total_natural_water = precip * growing_days
            irrigation_gap_mm = max(0, req["water_need_mm_total"] - total_natural_water)
            irrigation_cost_kes_per_ha = irrigation_gap_mm * 50  # ~KES 50/mm/ha irrigation cost

            results.append({
                "crop": crop.replace("_", " ").title(),
                "suitability_score": round(score, 2),
                "temp_c": temp.get("mean"),
                "precip_mm_day": precip,
                "solar_kwh_m2_day": solar,
                "soil_moisture": round(gwetroot_val, 2) if gwetroot_val else None,
                "soil_quality": soil_quality,
                "temp_suitable": temp_ok,
                "precip_suitable": precip_ok,
                "solar_suitable": solar_ok,
                "moisture_suitable": moisture_ok,
                "irrigation_gap_mm": round(irrigation_gap_mm),
                "irrigation_cost_kes_ha": round(irrigation_cost_kes_per_ha),
                "growing_days": growing_days,
            })

        results.sort(key=lambda r: r["suitability_score"], reverse=True)

        return {
            "latitude": latitude,
            "longitude": longitude,
            "county": county,
            "farm_size_ha": farm_size_ha,
            "crop_recommendations": results,
            "best_crop": results[0]["crop"] if results else None,
            "best_crop_score": results[0]["suitability_score"] if results else 0,
            "soil_health": self.SOIL_HEALTH_INDICATORS.get(soil_quality, {}),
        }

    async def estimate_yield(self, latitude: float, longitude: float, crop: str, farm_size_ha: float) -> dict:
        """Estimate yield (tonnes/ha) and expected revenue for a crop on this land."""
        suit = await self.analyse_land_suitability(latitude, longitude, "", farm_size_ha)
        crop_data = next((c for c in suit["crop_recommendations"] if c["crop"].lower() == crop.lower()), None)
        if not crop_data:
            return {"error": f"Crop {crop} not found in suitability analysis"}

        # Yield model: base yield * suitability factor * management factor
        base_yields_tonnes_ha = {
            "Maize": 2.5, "Beans": 1.2, "Tea": 3.0, "Coffee": 1.5,
            "Wheat": 2.0, "Sunflower": 1.8, "Drought Resistant Seed": 1.0,
            # Indigenous / traditional food plants (Maundu, 1999)
            "Amaranth": 3.0, "Black Nightshade": 2.5, "Spider Plant": 2.5,
            "Cowpea Leaves": 2.0, "Jute Mallow": 2.5, "Pumpkin Leaves": 3.0,
            "Finger Millet": 1.8, "Pigeon Pea": 1.5, "Bambara Nut": 1.2,
            "Sweet Potato": 4.0, "Cassava": 5.0, "Yam": 3.0,
            "Baobab": 0.5, "Tamarind": 0.8,
            # Ojwang (2020) — Homa Bay traditional crops
            "Dek": 2.5, "Mito": 2.5, "Boo": 3.0, "Atipa": 2.0, "Odielo": 2.5,
            "Ndemra": 2.5, "Alikra": 2.5, "Ng'Or": 1.5,
            "Mapera": 2.0, "Ochuoga": 1.0, "Akuno": 0.8, "Sangla": 0.8, "Nyatonglo": 0.8,
            "Slenderleaf": 2.5, "Desert Date": 0.8, "Bird Plum": 0.6, "Vitex Black Plum": 2.0,
        }
        base = base_yields_tonnes_ha.get(crop_data["crop"], 1.5)
        suitability_factor = 0.5 + 0.5 * crop_data["suitability_score"]
        yield_tonnes_ha = round(base * suitability_factor, 2)

        # Market prices (KES/tonne, conservative)
        market_prices_kes_tonne = {
            "Maize": 45000, "Beans": 85000, "Tea": 200000, "Coffee": 350000,
            "Wheat": 40000, "Sunflower": 60000, "Drought Resistant Seed": 80000,
            # Indigenous / traditional food plants (Maundu, 1999)
            "Amaranth": 60000, "Black Nightshade": 70000, "Spider Plant": 65000,
            "Cowpea Leaves": 55000, "Jute Mallow": 58000, "Pumpkin Leaves": 50000,
            "Finger Millet": 65000, "Pigeon Pea": 70000, "Bambara Nut": 80000,
            "Sweet Potato": 35000, "Cassava": 25000, "Yam": 45000,
            "Baobab": 150000, "Tamarind": 80000,
            # Ojwang (2020) — Homa Bay traditional crops
            "Dek": 55000, "Mito": 52000, "Boo": 50000, "Atipa": 48000, "Odielo": 53000,
            "Ndemra": 51000, "Alikra": 54000, "Ng'Or": 60000,
            "Mapera": 40000, "Ochuoga": 35000, "Akuno": 30000, "Sangla": 28000, "Nyatonglo": 32000,
            "Slenderleaf": 50000, "Desert Date": 120000, "Bird Plum": 90000, "Vitex Black Plum": 50000,
        }
        price_per_tonne = market_prices_kes_tonne.get(crop_data["crop"], 50000)

        total_yield = round(yield_tonnes_ha * farm_size_ha, 2)
        gross_revenue = round(total_yield * price_per_tonne)
        irrigation_cost = crop_data["irrigation_cost_kes_ha"] * farm_size_ha
        net_revenue = gross_revenue - irrigation_cost

        return {
            "crop": crop_data["crop"],
            "farm_size_ha": farm_size_ha,
            "yield_tonnes_ha": yield_tonnes_ha,
            "total_yield_tonnes": total_yield,
            "price_per_tonne_kes": price_per_tonne,
            "gross_revenue_kes": gross_revenue,
            "irrigation_cost_kes": round(irrigation_cost),
            "net_revenue_kes": net_revenue,
            "roi_percent": round((net_revenue / (irrigation_cost + 1)) * 100, 1) if irrigation_cost > 0 else 0,
        }

    async def detect_idle_land_risk(self, latitude: float, longitude: float) -> dict:
        """Detect if land appears idle or underutilised from vegetation index and moisture patterns."""
        veg = await self.power.get_vegetation_index(latitude, longitude)
        moist = await self.power.get_moisture_stress(latitude, longitude)
        solar = await self.power.get_solar_radiation(latitude, longitude)
        temp = await self.power.get_temperature(latitude, longitude)

        # Low vegetation + adequate moisture + high solar = likely idle/unplanted
        is_idle = veg < 0.3 and moist < 0.4 and solar > 4.0
        is_underutilised = veg < 0.45 and moist < 0.5

        return {
            "vegetation_index": veg,
            "moisture_stress": moist,
            "solar_kwh_m2_day": solar,
            "temp_mean": temp.get("mean"),
            "idle_risk": "idle" if is_idle else ("underutilised" if is_underutilised else "active"),
            "idle_confidence": round(1.0 - veg, 2),
            "recommendation": "This land appears suitable for planting. Consider drought-resistant seed varieties or contract farming."
            if is_idle else "Land appears in use. Monitor soil health for yield optimisation." if not is_underutilised
            else "Land may be underutilised. Consider intercropping or crop rotation to maximise value.",
        }
