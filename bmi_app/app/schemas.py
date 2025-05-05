from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class ProfileBase(BaseModel):
    age: Optional[int]
    gender: Optional[str]

class ProfileCreate(ProfileBase): pass
class ProfileOut(ProfileBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True

class BMIRecordBase(BaseModel):
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)

class BMIRecordCreate(BMIRecordBase): pass

class BMIRecordOut(BMIRecordBase):
    id: int
    bmi: float
    category: str
    created_at: datetime
    user_id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"