#!/usr/bin/env python3
"""KCW Demo Simulation — runs the full multi-agent pipeline
against 5 synthetic farmers and builds a securitisation pool.
"""

import asyncio
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import OrchestratorAgent
from agents.onboarding_agent import OnboardingAgent
from agents.credit_agent import CreditAssessmentAgent
from agents.geo_audit_agent import GeoAuditAgent
from agents.macro_climatic_agent import MacroClimaticAgent
from agents.verification_agent import VerificationAgent
from agents.procurement_agent import ProcurementAgent
from agents.liquidity_agent import LiquidityAgent
from services.risk_scoring import RiskScoringService
from services.securitisation import SecuritisationService

DEMO_FARMERS = [
    {
        "first_name": "Grace", "last_name": "Wanjiku",
        "phone": "+254712345001", "gender": "F",
        "county": "Kiambu", "sub_county": "Gatundu", "village": "Ithanga",
        "latitude": -1.0092, "longitude": 36.8990,
        "farm_size_ha": 3.0, "primary_crop": "maize", "year_registered": 2020,
        "chama_member": True, "sacco_member": True,
        "mpesa_monthly_velocity": 25000,
    },
    {
        "first_name": "Peter", "last_name": "Kiprop",
        "phone": "+254712345002", "gender": "M",
        "county": "Nakuru", "sub_county": "Molo", "village": "Elburgon",
        "latitude": -0.2919, "longitude": 35.9522,
        "farm_size_ha": 4.0, "primary_crop": "maize", "year_registered": 2022,
        "chama_member": False, "sacco_member": False,
    },
    {
        "first_name": "Samuel", "last_name": "Kipruto",
        "phone": "+254712345005", "gender": "M",
        "county": "Uasin Gishu", "sub_county": "Wareng", "village": "Kapsaret",
        "latitude": 0.5143, "longitude": 35.2698,
        "farm_size_ha": 5.0, "primary_crop": "maize", "year_registered": 2019,
        "chama_member": True, "sacco_member": True,
        "mpesa_monthly_velocity": 35000,
    },
    {
        "first_name": "Mary", "last_name": "Mutua",
        "phone": "+254712345006", "gender": "F",
        "county": "Machakos", "sub_county": "Masinga", "village": "Kangonde",
        "latitude": -1.2667, "longitude": 37.4667,
        "farm_size_ha": 2.0, "primary_crop": "beans", "year_registered": 2021,
        "chama_member": True, "sacco_member": False,
    },
    {
        "first_name": "Faith", "last_name": "Njeri",
        "phone": "+254712345010", "gender": "F",
        "county": "Nyeri", "sub_county": "Othaya", "village": "Kieni",
        "latitude": -0.2833, "longitude": 36.9500,
        "farm_size_ha": 2.5, "primary_crop": "tea", "year_registered": 2020,
        "chama_member": True, "sacco_member": True,
        "mpesa_monthly_velocity": 30000,
    },
]


async def main():
    print("=" * 60)
    print("  Kilimo Credit Web - Demo Simulation")
    print("  Multi-Agent Pipeline + Securitisation Pool")
    print("=" * 60)

    # Instantiate all agents
    orchestrator = OrchestratorAgent(
        onboarding=OnboardingAgent(),
        credit=CreditAssessmentAgent(risk_scorer=RiskScoringService()),
        geo=GeoAuditAgent(),
        climatic=MacroClimaticAgent(),
        verification=VerificationAgent(),
        procurement=ProcurementAgent(),
        liquidity=LiquidityAgent(securitisation=SecuritisationService()),
    )

    approved_farmers = []

    for i, farmer_data in enumerate(DEMO_FARMERS, 1):
        print(f"\n{'-' * 50}")
        print(f"  [{i}/{len(DEMO_FARMERS)}] Processing: {farmer_data['first_name']} {farmer_data['last_name']}")
        print(f"  County: {farmer_data['county']} | Crop: {farmer_data['primary_crop']} | Gender: {farmer_data['gender']}")

        result = await orchestrator.process_farmer_application(farmer_data)

        print(f"  Status: {result['status'].upper()}")
        print(f"  Credit Score: {result.get('assessment', {}).get('credit_score', 'N/A')}")
        print(f"  PD: {result.get('assessment', {}).get('probability_default', 'N/A')}")
        print(f"  Max Loan: KES {result.get('assessment', {}).get('max_loan_kes', 0):,.0f}")
        print(f"  Elapsed: {result.get('elapsed_seconds', 0):.2f}s")

        if result["status"] == "approved":
            approved_farmers.append(result)

    print(f"\n{'=' * 50}")
    print(f"  Approved: {len(approved_farmers)} / {len(DEMO_FARMERS)} farmers")
    print(f"{'=' * 50}")

    if approved_farmers:
        print(f"\n  Building securitisation pool from {len(approved_farmers)} approved farmers...")
        pool_data = []
        for af in approved_farmers:
            ass = af.get("assessment", {})
            pool_data.append({
                "id": af.get("farmer_id", "unknown"),
                "max_loan_kes": ass.get("max_loan_kes", 0),
                "probability_default": ass.get("probability_default", 0),
                "interest_rate_annual": 18.0,
            })
        pool = await orchestrator.assemble_pool(pool_data)
        print(f"  Pool ID: {pool.get('id', 'N/A')}")
        print(f"  Farmers: {pool.get('farmer_count', 0)}")
        print(f"  Total Notional: KES {pool.get('total_notional_kes', 0):,.0f}")
        print(f"  Avg PD: {pool.get('avg_pd', 0):.2%}")
        print(f"  Expected Revenue: KES {pool.get('expected_revenue_kes', 0):,.0f}")
        print(f"  Target Rating: {pool.get('target_rating', 'N/A')}")

    print(f"\n{'=' * 50}")
    print("  Demo complete.")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    asyncio.run(main())
