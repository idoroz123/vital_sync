from pydantic import BaseModel, Field, condecimal
from datetime import date
from typing import Optional


class SleepActivityBase(BaseModel):
    total_sleep_duration: condecimal(max_digits=4, decimal_places=2)
    sleep_quality: str = Field(..., max_length=50)
    deep_sleep_duration: condecimal(max_digits=4, decimal_places=2)
    wake_up_count: int = Field(..., ge=0)

    class Config:
        from_attributes = True


class SleepActivityCreate(SleepActivityBase):
    recorded_at: date


class SleepActivityUpdate(BaseModel):
    total_sleep_duration: Optional[condecimal(max_digits=4, decimal_places=2)] = None
    sleep_quality: Optional[str] = Field(None, max_length=50)
    deep_sleep_duration: Optional[condecimal(max_digits=4, decimal_places=2)] = None
    wake_up_count: Optional[int] = Field(None, ge=0)


class SleepActivityResponse(SleepActivityBase):
    id: int
    user_id: int
    recorded_at: date
