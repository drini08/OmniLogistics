from pydantic import BaseModel
from typing import Optional

class DriverBase(BaseModel):
    full_name: str
    license_category: str
    contact_number: str
    is_active: bool = True

class DriverCreate(DriverBase):
    password: str

class DriverResponse(DriverBase):
    id: int
    role: str = "Driver"

    class Config:
        from_attributes = True

class Driver(DriverBase):
    id: int