from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.seller.seller_schema import NewProduct
from src.models.seller_models.sellerProduct_model import SellerProduct
from src.db import get_session


seller_router = APIRouter(prefix="/seller", tags=["/seller"])


@seller_router.post("/new_product")
async def newProduct(data_product: NewProduct, session:AsyncSession = Depends(get_session)):
    
    new_product = SellerProduct(**data_product.model_dump())
    
    session.add(new_product)
    await session.commit()
    
    return new_product