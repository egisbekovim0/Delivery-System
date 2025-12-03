from pydantic import BaseModel, Field
from app.database.models import ShipmentStatus

class BaseShipment(BaseModel):
    content: str 
    weight: float = Field(le=25)

class ShipmentRead(BaseShipment):
    status: ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus