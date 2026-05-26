import uuid
from datetime import datetime, timezone
from typing import Optional

from .onboarding_agent import OnboardingAgent
from .credit_agent import CreditAssessmentAgent
from .geo_audit_agent import GeoAuditAgent
from .macro_climatic_agent import MacroClimaticAgent
from .verification_agent import VerificationAgent
from .procurement_agent import ProcurementAgent
from .liquidity_agent import LiquidityAgent


class OrchestratorAgent:
    """Central orchestrator coordinating the full KCW multi-agent workflow.

    Manages the pipeline: Onboarding -> Geo-Audit -> Macro-Climatic ->
    Credit Assessment -> V&V -> Procurement/Settlement.
    """

    def __init__(
        self,
        onboarding: OnboardingAgent,
        credit: CreditAssessmentAgent,
        geo: GeoAuditAgent,
        climatic: MacroClimaticAgent,
        verification: VerificationAgent,
        procurement: ProcurementAgent,
        liquidity: LiquidityAgent,
    ):
        self.onboarding = onboarding
        self.credit = credit
        self.geo = geo
        self.climatic = climatic
        self.verification = verification
        self.procurement = procurement
        self.liquidity = liquidity
        self.session_id = str(uuid.uuid4())

    async def process_farmer_application(
        self, raw_input: dict
    ) -> dict:
        workflow_id = str(uuid.uuid4())
        start_time = datetime.now(timezone.utc)

        # Step 1: Onboarding — parse raw farmer data
        farmer_profile = await self.onboarding.ingest(raw_input)

        # Step 2: Geo-audit — verify location, soil, vegetation
        geo_report = await self.geo.audit(farmer_profile)

        # Step 3: Macro-climatic — climate stress overlay
        climate_report = await self.climatic.assess(farmer_profile)

        # Step 4: Credit assessment — PD_i logistic regression + Featherless
        assessment = await self.credit.assess(
            farmer_profile, geo_report, climate_report
        )

        # Step 5: V&V agent — verify consistency across all outputs
        verification = await self.verification.verify(
            farmer_profile=farmer_profile,
            geo_report=geo_report,
            climate_report=climate_report,
            assessment=assessment,
        )
        if not verification["passed"]:
            return {
                "workflow_id": workflow_id,
                "status": "rejected",
                "reason": "V&V checks failed",
                "inconsistencies": verification["inconsistencies"],
                "elapsed_seconds": (datetime.now(timezone.utc) - start_time).total_seconds(),
            }

        # Step 6: If approved, initiate procurement & settlement
        if assessment.get("approved", False):
            settlement = await self.procurement.disburse(
                farmer_profile, assessment
            )
            return {
                "workflow_id": workflow_id,
                "status": "approved",
                "farmer_id": farmer_profile.get("id"),
                "assessment": assessment,
                "settlement": settlement,
                "elapsed_seconds": (datetime.now(timezone.utc) - start_time).total_seconds(),
            }

        return {
            "workflow_id": workflow_id,
            "status": "declined",
            "farmer_id": farmer_profile.get("id"),
            "assessment": assessment,
            "elapsed_seconds": (datetime.now(timezone.utc) - start_time).total_seconds(),
        }

    async def assemble_pool(self, assessments: list[dict]) -> dict:
        pool_data = [
            {
                "id": a.get("farmer_id") or a.get("id", "unknown"),
                "max_loan_kes": a.get("max_loan_kes", 0),
                "probability_default": a.get("probability_default", 0),
                "interest_rate_annual": 18.0,
                "loan_id": f"LN-{a.get('farmer_id', 'unknown')}",
            }
            for a in assessments
        ]
        return await self.liquidity.assemble_pool(pool_data)
