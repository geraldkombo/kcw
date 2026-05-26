import pytest
from masumi.escrow_lifecycle import EscrowLifecycle, EscrowState
from masumi.mip003_api import InputSchema, generate_mip003_endpoints


class TestEscrowLifecycle:
    def test_initial_state(self):
        escrow = EscrowLifecycle("ESC-001")
        assert escrow.state == EscrowState.FUNDS_LOCKING_REQUESTED
        assert len(escrow.history) == 1

    def test_valid_transition(self):
        escrow = EscrowLifecycle("ESC-001")
        escrow.state = EscrowState.FUNDS_LOCKED
        assert escrow.state == EscrowState.FUNDS_LOCKED
        assert len(escrow.history) == 2

    def test_complete_lifecycle(self):
        escrow = EscrowLifecycle("ESC-002")
        escrow.state = EscrowState.FUNDS_LOCKED
        escrow.state = EscrowState.RESULT_SUBMITTED
        escrow.state = EscrowState.COMPLETED
        assert escrow.state == EscrowState.COMPLETED
        assert len(escrow.history) == 4

    def test_refund_authorized_lifecycle(self):
        escrow = EscrowLifecycle("ESC-003")
        escrow.state = EscrowState.FUNDS_LOCKED
        escrow.state = EscrowState.RESULT_SUBMITTED
        escrow.state = EscrowState.REFUND_AUTHORIZED
        escrow.state = EscrowState.REFUNDED
        assert escrow.state == EscrowState.REFUNDED
        assert len(escrow.history) == 5

    def test_invalid_transition_raises(self):
        escrow = EscrowLifecycle("ESC-004")
        with pytest.raises(ValueError, match="Invalid transition"):
            escrow.state = EscrowState.COMPLETED  # skip FUNDS_LOCKED

    def test_invalid_refund_authorized_transition_raises(self):
        escrow = EscrowLifecycle("ESC-005")
        with pytest.raises(ValueError, match="Invalid transition"):
            escrow.state = EscrowState.REFUND_AUTHORIZED  # can't jump from initial

    def test_to_dict(self):
        escrow = EscrowLifecycle("ESC-004")
        d = escrow.to_dict()
        assert d["escrow_id"] == "ESC-004"
        assert d["current_state"] == "FundsLockingRequested"
        assert len(d["history"]) == 1


class TestMIP003:
    def test_generate_endpoints(self):
        schema = InputSchema(
            properties={"name": {"type": "string"}},
            required=["name"],
        )
        endpoints = generate_mip003_endpoints("credit-agent", schema)
        assert "input_schema" in endpoints
        assert endpoints["start_job"] == "/api/v1/credit-agent/start_job"
        assert endpoints["availability"] == "/api/v1/credit-agent/availability"
