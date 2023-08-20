from typing import Optional
from pydantic import BaseModel

from stockdorshared.models.JobStates import JobStates


class ComputeStats(BaseModel):
    state: Optional[JobStates]
    state_message: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    compute_duration: Optional[float]