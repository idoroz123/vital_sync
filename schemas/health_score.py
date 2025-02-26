from pydantic import BaseModel
from typing import Dict


class HealthScoreResponse(BaseModel):
    user_id: int
    health_score: float
    details: Dict[str, float]
