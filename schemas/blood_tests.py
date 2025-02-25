from pydantic import BaseModel, Field, condecimal
from datetime import date
from typing import Optional


class BloodTestBase(BaseModel):
    glucose_level: Optional[condecimal(max_digits=5, decimal_places=2)]
    cholesterol: Optional[condecimal(max_digits=5, decimal_places=2)]
    hemoglobin: Optional[condecimal(max_digits=5, decimal_places=2)]
    blood_pressure: Optional[str] = Field(None, max_length=10)
    triglycerides: Optional[condecimal(max_digits=5, decimal_places=2)]

    class Config:
        from_attributes = True


class BloodTestCreate(BloodTestBase):
    test_date: date


class BloodTestUpdate(BaseModel):
    glucose_level: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    cholesterol: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    hemoglobin: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    blood_pressure: Optional[str] = Field(None, max_length=10)
    triglycerides: Optional[condecimal(max_digits=5, decimal_places=2)] = None


class BloodTestResponse(BloodTestBase):
    id: int
    user_id: int
    test_date: date
