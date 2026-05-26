"""MIP-003 Agentic Service API Standard compliance.
Implements /input_schema, /start_job, /status, /availability endpoints.
"""

from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Any


class InputSchema(BaseModel):
    """Describes the input schema for an agentic service (MIP-003)."""
    type: str = "object"
    properties: dict[str, Any]
    required: list[str]


class StartJobRequest(BaseModel):
    """POST /start_job payload (MIP-003)."""
    agent_id: str
    input_data: dict[str, Any]
    callback_url: str = ""
    idempotency_key: str = ""


class StartJobResponse(BaseModel):
    """Response from /start_job."""
    job_id: str
    status: str = "accepted"
    estimated_completion_seconds: int = 30


class JobStatusResponse(BaseModel):
    """GET /status/{job_id} response."""
    job_id: str
    status: str  # pending, running, completed, failed
    result: dict[str, Any] = Field(default_factory=dict)
    error: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None


class AvailabilityResponse(BaseModel):
    """GET /availability response."""
    agent_id: str
    available: bool = True
    rate_limit_per_minute: int = 60
    current_load: int = 0
    max_concurrent_jobs: int = 10


# ---- MIP-003 endpoint generator (conceptual) ----
# pip-masumi Endpoint Abstraction (2026) auto-generates
# these endpoints from ~20 lines of config.
# Reference: github.com/masumi-network/pip-masumi

def generate_mip003_endpoints(agent_id: str, input_schema: InputSchema):
    """Returns endpoint stubs matching MIP-003 spec."""
    return {
        "input_schema": input_schema.model_dump(),
        "start_job": f"/api/v1/{agent_id}/start_job",
        "status": f"/api/v1/{agent_id}/status/{{job_id}}",
        "availability": f"/api/v1/{agent_id}/availability",
    }
