from pydantic import BaseModel, Field, EmailStr, condecimal
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr
    age: int = Field(..., ge=18, le=120)
    gender: str = Field(..., max_length=10)
    height: condecimal(max_digits=5, decimal_places=2)  # e.g. 175.25
    weight: condecimal(max_digits=5, decimal_places=2)  # e.g. 70.5

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr]
    age: Optional[int] = Field(None, ge=18, le=120)
    gender: Optional[str] = Field(None, max_length=10)
    height: Optional[condecimal(max_digits=5, decimal_places=2)]
    weight: Optional[condecimal(max_digits=5, decimal_places=2)]

    class Config:
        orm_mode = True
