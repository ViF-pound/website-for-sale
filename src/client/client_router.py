from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.client.client_schema import Review
from src.db import get_session
from src.get_current_user import get_current_id
from src.models.user_model import User
from src.models.seller_models.sellerProduct_model import SellerProduct
from src.models.seller_models.seller_model import Seller

client_router = APIRouter(prefix="/client", tags=["client"])


@client_router.get("/products")
async def get_products(session:AsyncSession = Depends(get_session)):

    products = await session.scalars(select(SellerProduct).options(selectinload(SellerProduct.product), selectinload(SellerProduct.seller)))

    return products.all()


@client_router.post("/review/add")
async def review_add(data_review: Review, user_id:int = Depends(get_current_id),  session:AsyncSession = Depends(get_session)):

    if not user_id:
        raise HTTPException(status_code=401, detail="not auth")

    new_review = Review(**data_review.model_dump())

    if not new_review.estimation:
        raise HTTPException(status_code=400, detail="incorect estimation")

    session.add(new_review)
    session.commit()

    return new_review


@client_router.delete("/review/delete")
async def review_delete(id_review: int, user_id: int = Depends(get_current_id), session:AsyncSession = Depends(get_session)):

    if not user_id:
         raise HTTPException(status_code=401, detail="not auth")
    
    review = await session.scalar(select(Review).where(Review.id == id_review))

    if not review.estimation:
        raise HTTPException(status_code=400, detail="incorect estimation")

    session.delete(review)
    session.commit()

    return {"message": "review delete"}


@client_router.get("/review/all")
async def get_reviews(seller_id:int = Depends(get_current_id), session:AsyncSession = Depends(get_session)):

    seller = await session.scalar(select(Seller).options(selectinload(Seller.reviews)).where(Seller.id == seller_id))

    if not seller:
        raise HTTPException(status_code=426, detail="no data found")

    return seller.reviews


#@client_router.get("/backet/product/add")


#@client_router.get("/backet/product/delete")


#@client_router.get("/backet/delete_all")


#@client_router.get("/backet/pay")