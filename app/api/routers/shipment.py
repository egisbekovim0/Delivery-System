from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import SellerDep, ShipmentServiceDep
from app.api.schemas.shipment import ShipmentRead, ShipmentCreate, ShipmentUpdate

router = APIRouter(prefix="/shipment", tags=["Shipment"])

@router.get("/", response_model=ShipmentRead)
async def get_shipment(id: UUID,  service: ShipmentServiceDep):

    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="given id doesn't exist"
        )
    return shipment


@router.post("/", response_model=ShipmentRead)
async def submit_shipment(seller: SellerDep, 
            shipment: ShipmentCreate, 
            service: ShipmentServiceDep):
    return await service.add(shipment, seller)


@router.patch("/", response_model=ShipmentRead)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ShipmentServiceDep):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='no data provided for the update'
        )
    return await service.update(id, update)


@router.delete("/")
async def delete_shipment(id: int, service: ShipmentServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"detail": f"shipment with id {id} is deleted"}

