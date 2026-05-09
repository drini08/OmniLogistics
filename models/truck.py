from pydantic import BaseModel
from typing import Optional

class TruckBase(BaseModel):
    license_plate: str
    model_name: str
    max_load_capacity: float
    current_mileage: float = 0.0

class TruckCreate(TruckBase):
    pass

class TruckResponse(TruckBase):
    id: int
    status: str = "Healthy"

    class Config:
        from_attributes = True

class Truck(TruckBase):
    id: int