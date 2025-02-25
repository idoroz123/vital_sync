from pydantic import BaseModel, Field, condecimal
from datetime import date
from typing import Optional


class PhysicalActivityBase(BaseModel):
    steps: int = Field(..., ge=0)
    calories_burned: int = Field(..., ge=0)
    workout_duration: condecimal(max_digits=4, decimal_places=2)
    activity_type: Optional[str] = Field(None, max_length=50)

    class Config:
        from_attributes = True


class PhysicalActivityCreate(PhysicalActivityBase):
    recorded_at: date


class PhysicalActivityUpdate(BaseModel):
    steps: Optional[int] = Field(None, ge=0)
    calories_burned: Optional[int] = Field(None, ge=0)
    workout_duration: Optional[condecimal(max_digits=4, decimal_places=2)] = None
    activity_type: Optional[str] = Field(None, max_length=50)


class PhysicalActivityResponse(PhysicalActivityBase):
    id: int
    user_id: int
    recorded_at: date
