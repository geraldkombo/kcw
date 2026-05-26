import uuid
from typing import Optional

from masumi.x402_client import MasumiX402Client


class ProcurementAgent:
    """Procurement Agent — handles loan disbursement via Masumi x402 escrow.
    Disburses KES-equivalent in USDM (Moneta stablecoin) through Cardano escrow.
    """

    def __init__(self, masumi: Optional[MasumiX402Client] = None):
        self.masumi = masumi

    async def disburse(self, farmer_profile: dict, assessment: dict) -> dict:
        loan_amount = assessment.get("max_loan_kes", 0)
        farmer_id = farmer_profile.get("id", "unknown")
        txn_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"

        result = {
            "transaction_id": txn_id,
            "farmer_id": farmer_id,
            "amount_kes": loan_amount,
            "status": "simulated",
            "message": f"Loan of KES {loan_amount:,.0f} approved for {farmer_profile.get('first_name')} "
                       f"{farmer_profile.get('last_name')} ({farmer_id})",
            "disbursement_channel": "M-Pesa",
        }

        if self.masumi:
            try:
                # Simulate x402 payment: KES approximated as USDM at 1 USDM = 130 KES
                lovelace_amount = int(loan_amount / 130 * 1_000_000)
                async def _send_data():
                    return {
                        "farmer_id": farmer_id,
                        "amount": loan_amount,
                        "currency": "KES",
                    }

                escrow = await self.masumi.x402_pay_for_data(
                    amount_lovelace=max(lovelace_amount, 1_000_000),
                    data_description=f"Loan disbursement to {farmer_id}",
                    data_callback=_send_data,
                )
                result["masumi_escrow_id"] = escrow.get("escrow_id")
                result["masumi_state"] = escrow.get("final_state")
                result["status"] = "disbursed"
            except Exception as e:
                result["status"] = "escrow_failed"
                result["error"] = str(e)

        return result
