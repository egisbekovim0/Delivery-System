from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import DeliveryPartnerDep, SellerServiceDep, get_access_token, get_partner_access_token
from app.api.schemas.delivery_partner import DeliveryPartnerUpdate
from app.database.redis import add_jti_to_blacklist
from ..schemas.seller import DeliveryPartnerCreate, DeliveryPartnerRead

router = APIRouter(prefix="/partner", tags=["Delivery partner"])


@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(seller: DeliveryPartnerCreate, 
                                    service): 
    return await service.add(seller)

@router.post("/token")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt"
    }

@router.post("/")
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service,
):
    pass

@router.get("/logout")
async def logout_delivery_partner(token_data: Annotated[dict, Depends(get_partner_access_token)]):
    await add_jti_to_blacklist(token_data["jti"])
    return {
        "detail": "successfully logged out"
    }