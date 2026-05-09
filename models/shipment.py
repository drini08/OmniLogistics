from pydantic import BaseModel
from typing import Optional

class ShipmentBase(BaseModel):
    origin: str
    destination: str
    cargo_weight: float
    truck_id: int
    driver_id: int

class ShipmentCreate(ShipmentBase):
    pass

# THIS IS THE MISSING CLASS:
class ShipmentUpdate(BaseModel):
    status: Optional[str] = None
    destination: Optional[str] = None
    cargo_weight: Optional[float] = None

class ShipmentResponse(ShipmentBase):
    id: int
    status: str

    class Config:
        from_attributes = True