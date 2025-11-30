from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate
from .database import shipments, save

app = FastAPI()

@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="given id doesn't exist"
        )
    return shipments[id]


@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        **shipment.model_dump(),
        "id": new_id,
        "status": "placed",
    }
    save()
    return {"id": new_id}


@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> dict[str, Any]:
    return {field: shipments[id][field]}


@app.patch("/shipment", response_model=ShipmentRead)
def shipment_update(id: int, body: ShipmentUpdate):
    shipments[id].update(body.model_dump(exclude_none=True))
    save()
    return shipments[id]


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)
    return {"detail": f"shipment with id {id} is deleted"}


# for api documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():

    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
