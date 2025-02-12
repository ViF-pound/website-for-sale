from fastapi import APIRouter, HTTPException

from sqlalchemy import select

from src.seller.seller_shema import NewProduct, Review
from src.seller.seller_models import SellerProduct
from src.db import session


seller_router = APIRouter(prefix="/seller", tags=["/seller"])


@seller_router.post("/new_product")
async def newProduct(data_product: NewProduct):
    
    new_product = SellerProduct(name = data_product.name, description = data_product.description, price = data_product.price, curenccy = data_product.currency)
    
    session.add(new_product)
    session.commit()
    
    return {"message": "product created successfully"}


@seller_router.post("/review")
async def review(data_review: Review):

    new_review = Review(seller_id = data_review.seller_id, estimation = data_review.estimation, text = data_review.text)

    if new_review.estimation != True and new_review.estimation != False:
        raise HTTPException(status_code=400, detail="incorect estimation")

    session.add(new_review)
    session.commit()

    return {"message": "review left"}