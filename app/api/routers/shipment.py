from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import ServiceDep
from app.api.schemas.shipment import Shipment, ShipmentCreate, ShipmentUpdate

router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/", response_model=Shipment)
async def get_shipment(id: int, service: ServiceDep):

    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="given id doesn't exist"
        )
    return shipment


@router.post("/")
async def submit_shipment(shipment: ShipmentCreate, service: ServiceDep)-> Shipment:
    return await service.add(shipment)


@router.patch("/", response_model=Shipment)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ServiceDep):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='no data provided for the update'
        )
    shipment = await service.update(id, update)


    return shipment


@router.delete("/")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"detail": f"shipment with id {id} is deleted"}

