from typing import List
from pydantic import BaseModel, EmailStr, constr,validator
from datetime import datetime

class CustBaseSchema(BaseModel):
    title: str
    name: str
    gender: str
    marital_status: str
    phone: str
    email: EmailStr

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class CustUpdBaseSchema(BaseModel):
    
    title: str
    name: str
    gender: str
    marital_status: str
    phone: str
    email: EmailStr
    updated_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }

class ListCustResponse(BaseModel):
    status: str
    results: int
    customers: List[CustBaseSchema]

class UserBaseSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)