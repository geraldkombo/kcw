from __future__ import annotations

from typing import Optional

from agents.orchestrator import OrchestratorAgent
from agents.onboarding_agent import OnboardingAgent
from agents.credit_agent import CreditAssessmentAgent
from agents.geo_audit_agent import GeoAuditAgent
from agents.macro_climatic_agent import MacroClimaticAgent
from agents.verification_agent import VerificationAgent
from agents.procurement_agent import ProcurementAgent
from agents.liquidity_agent import LiquidityAgent
from featherless.client import FeatherlessClient
from masumi.x402_client import MasumiX402Client
from satellite.power_client import PowerClient
from services.risk_scoring import RiskScoringService
from services.securitisation import SecuritisationService
from services.reporting import AuditTrail
from database.repository import Repository, create_repository

_featherless: Optional[FeatherlessClient] = None
_masumi: Optional[MasumiX402Client] = None
_power: Optional[PowerClient] = None
_orchestrator: Optional[OrchestratorAgent] = None
_audit: Optional[AuditTrail] = None
_securitisation: Optional[SecuritisationService] = None
_repository: Optional[Repository] = None


def get_featherless() -> Optional[FeatherlessClient]:
    global _featherless
    if _featherless is None:
        try:
            _featherless = FeatherlessClient()
        except ValueError:
            _featherless = None
    return _featherless


def get_power() -> PowerClient:
    global _power
    if _power is None:
        _power = PowerClient()
    return _power


def get_masumi() -> MasumiX402Client:
    global _masumi
    if _masumi is None:
        _masumi = MasumiX402Client()
    return _masumi


def get_audit() -> AuditTrail:
    global _audit
    if _audit is None:
        _audit = AuditTrail()
    return _audit


def get_securitisation() -> SecuritisationService:
    global _securitisation
    if _securitisation is None:
        _securitisation = SecuritisationService()
    return _securitisation


def get_repository() -> Repository:
    global _repository
    if _repository is None:
        _repository = create_repository()
    return _repository


def get_orchestrator() -> OrchestratorAgent:
    global _orchestrator
    if _orchestrator is None:
        featherless = get_featherless()
        masumi = get_masumi()
        power = get_power()
        risk_scorer = RiskScoringService()
        _orchestrator = OrchestratorAgent(
            onboarding=OnboardingAgent(featherless=featherless),
            credit=CreditAssessmentAgent(risk_scorer=risk_scorer, featherless=featherless),
            geo=GeoAuditAgent(featherless=featherless, power=power),
            climatic=MacroClimaticAgent(power=power),
            verification=VerificationAgent(),
            procurement=ProcurementAgent(masumi=masumi),
            liquidity=LiquidityAgent(securitisation=get_securitisation()),
        )
    return _orchestrator
