from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.seller.seller_schema import NewProduct
from src.models.seller_models.sellerProduct_model import SellerProduct
from src.db import get_session
from src.get_current_user import get_current_user
from src.models.user_model import User
from src.models.seller_models.seller_model import Seller


seller_router = APIRouter(prefix="/seller", tags=["/seller"])


@seller_router.post("/seller/create")
async def newSeller(profile:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):

    if profile.seller:
        raise HTTPException(status_code=426, detail="You have profile")
    
    new_seller = Seller()

    session.add(new_seller)
    await session.flush(new_seller)
    await session.commit

    return new_seller



@seller_router.post("/product/create")
async def newProduct(data_product: NewProduct, session:AsyncSession = Depends(get_session)):
    
    new_product = SellerProduct(**data_product.model_dump())
    
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    
    return new_product