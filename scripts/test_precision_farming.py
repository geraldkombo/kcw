"""Quick test for precision farming module — equatorial general agriculture intelligence."""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agriculture_intelligence.precision_farming import PrecisionFarming

async def test():
    pf = PrecisionFarming()

    print("=== GROWING DEGREE DAYS (Rose, Naivasha) ===")
    r = await pf.compute_gdd(-0.7, 36.4, "rose")
    print(f"GDD/day: {r['gdd_per_day']} | Days to harvest: {r['estimated_days_to_harvest']} | {r['harvest_readiness']}")

    print("\n=== FAO-56 ET (Kiambu) ===")
    r = await pf.compute_et_penman_monteith(-1.0, 36.9)
    print(f"ET0: {r['et0_mm_day']} mm/day | Precision irrigation: {r['precision_irrigation_needed']}")

    print("\n=== PEST/DISEASE RISK (Rose) ===")
    r = await pf.assess_pest_disease_risk(-0.7, 36.4, "rose")
    print(f"Risk: {r['overall_risk']} | Active: {r['total_risk_count']}")
    for risk in r.get("active_risks", []):
        print(f"  {risk['pest']}: {risk['risk_score']}/100 ({risk['risk_level']})")

    print("\n=== MICRO-CLIMATE ZONE ===")
    r = await pf.classify_micro_climate(-1.0, 36.9)
    print(f"Zone: {r['zone']} — Recommended: {r['recommended_crops']}")

    print("\n=== FROST RISK (Highland) ===")
    r = await pf.assess_frost_risk(-0.3, 36.8)
    print(f"Frost: {r['frost_risk']} at {r['min_temp_c']}C")

    print("\n=== PRECISION IRRIGATION TIMING ===")
    r = await pf.get_precision_irrigation_timing(-1.0, 36.9)
    print(f"Best time: {r['optimal_irrigation_time']} | Saves {r['water_saved_by_timing_pct']}%")

    print("\n=== VARIABLE RATE (2.5ha) ===")
    r = await pf.get_variable_rate_recommendation(-1.0, 36.9, 2.5)
    print(f"Saves {r['water_saving_vs_uniform_pct']}% vs uniform")
    for z in r["zones"]:
        print(f"  Zone {z['zone']}: {z['area_ha']}ha, moisture={z['moisture_fraction']}, {z['recommendation']}")

if __name__ == "__main__":
    asyncio.run(test())
