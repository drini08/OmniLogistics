from pydantic import BaseModel
from typing import Optional

class ShipmentBase(BaseModel):
    origin: str = "Prishtina"
    destination: str
    cargo_weight: float
    truck_id: int
    driver_id: int

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentResponse(ShipmentBase):
    id: int
    status: str = "Scheduled"

    class Config:
        from_attributes = True

class Shipment(ShipmentBase):
    id: int