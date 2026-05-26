"""KCW Investment Advisor Demo — shows the full agricultural investment intelligence system."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from agents.investment_advisor_agent import InvestmentAdvisorAgent

async def demo():
    agent = InvestmentAdvisorAgent()
    result = await agent.recommend({
        'id': 'KCW-DEMO-001',
        'latitude': -1.0, 'longitude': 36.9, 'county': 'Kiambu',
        'farm_size_ha': 2.5, 'budget_kes': 500000,
        'primary_crop': 'maize', 'dairy_cows': 2,
        'chama_member': True, 'sacco_member': True,
        'mpesa_monthly_velocity': 15000,
    })
    r = result['recommendations']
    print('=' * 60)
    print('  KCW AI Agriculture Investment Advisor')
    print('=' * 60)
    print(f'\nLocation: {r["location"]["county"]} ({r["location"]["latitude"]}, {r["location"]["longitude"]})')
    print(f'Farm Size: {r["farm_size_ha"]}ha | Budget: KES {r["budget_kes"]:,}')
    print(f'Best Crop: {r["recommended_crop"]}')
    print(f'Equatorial Solar Advantage: +{r["equatorial_solar_advantage_pct"]}% vs temperate')
    print(f'Water Deficit: {r["current_water_deficit_mm_day"]}mm/day')
    print(f'Idle Land: {r["idle_land_status"]}')
    print(f'Soil Health: {r["soil_health"]}')
    print(f'\nInvestment Opportunities ({len(r["ranked_opportunities"])} found):')
    print('-' * 60)
    for opp in r['ranked_opportunities']:
        print(f'  [{opp["roi_pct"]:>6.1f}% ROI] {opp["name"]}')
        print(f'           Invest KES {opp["investment_kes"]:>8,} -> Return KES {opp["expected_return_kes"]:>8,}')
        print(f'           Risk: {opp["risk"]} | {opp["timeframe_months"]} months')
    print('-' * 60)
    print(f'\nPortfolio Summary:')
    print(f'  Total Investment: KES {r["total_investment_kes"]:>8,}')
    print(f'  Expected Return:  KES {r["total_expected_return_kes"]:>8,}')
    print(f'  Portfolio ROI:    {r["portfolio_roi_pct"]:>6.1f}%')
    if r.get('best_first_investment'):
        b = r['best_first_investment']
        print(f'\n  Recommended First Step: {b["name"]}')
        print(f'    Invest KES {b["investment_kes"]:,} for {b["roi_pct"]}% ROI in {b["timeframe_months"]} months')
    print(f'\nInvestment Readiness: {result["investment_readiness"]["level"]} ({result["investment_readiness"]["score"]}/100)')
    print('\n' + '=' * 60)
    print('  KCW: Systems, not apps. AI makes agriculture investments.')
    print('=' * 60)

if __name__ == '__main__':
    asyncio.run(demo())
