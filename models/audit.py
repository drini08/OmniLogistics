from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuditBase(BaseModel):
    timestamp: datetime = datetime.now()
    actor_id: int
    action_type: str
    affected_entity: str
    before_value: Optional[str] = None
    after_value: Optional[str] = None

class AuditCreate(AuditBase):
    pass

class AuditResponse(AuditBase):
    id: int

    class Config:
        from_attributes = True

class Audit(AuditBase):
    id: int

