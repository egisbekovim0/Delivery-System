from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from app.database.models import ShipmentStatus

class BaseShipment(SQLModel):
    content: str
    weight: float = Field(le=25)
    destination: int

class ShipmentRead(BaseShipment):
    id: int
    status: ShipmentStatus
    estimated_delivery: datetime
    
class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)