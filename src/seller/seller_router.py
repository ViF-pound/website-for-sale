import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.cosntants.constants import UPLOAD_FOLDER
from src.seller.seller_schema import NewProduct, NewSeller
from src.models.seller_models.sellerProduct_model import SellerProduct
from src.db import get_session
from src.get_current_user import get_current_user, get_current_confirm_seller
from src.models.user_model import User
from src.models.seller_models.seller_model import Seller


seller_router = APIRouter(prefix="/seller", tags=["/seller"])


@seller_router.post("/create")
async def newSeller(data_seller: NewSeller, user:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):

    if user.seller:
        raise HTTPException(status_code=426, detail="You have profile")
    
    seller = await session.scalar(select(Seller).where(Seller.seller_name == data_seller.seller_name))
    if seller:
        raise HTTPException(status_code=400, detail="This name is busy")
    
    new_seller = Seller(**data_seller.model_dump())

    session.add(new_seller)
    await session.commit()
    await session.refresh(new_seller)

    return new_seller


@seller_router.get("/products")
async def seller_products(user:User = Depends(get_current_confirm_seller), session: AsyncSession = Depends(get_session)):

    products = session.scalars(select(SellerProduct).where(SellerProduct.seller == user.seller).options(selectinload(SellerProduct.product)))

    return products.all()


@seller_router.post("/product/create")
async def newProduct(data_product: NewProduct, user: User = Depends(get_current_confirm_seller), session: AsyncSession = Depends(get_session)):

    new_product = SellerProduct(**data_product.model_dump())
    
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    
    return new_product


@seller_router.delete("/product/selete")
async def delete_product(id:int, user:User = Depends(get_current_confirm_seller), session: AsyncSession = Depends(get_session)):

    product = session.scalar(select(select(SellerProduct).where(SellerProduct.id == id).options(selectinload(SellerProduct.seller))))
    if user.seller != product.seller:
        raise HTTPException(status_code=403, detail="you are not seller of this product")
    
    await session.delete(product)
    await session.commit()

    return {"producte delete"}
    

@seller_router.post("/product/create/image")
async def create_product_image(product_id:int,file: UploadFile = File(...), user:User = Depends(get_current_confirm_seller), session:AsyncSession = Depends(get_session)):

    product = await session.scalar(select(SellerProduct).where(SellerProduct.id == product_id).options(selectinload(SellerProduct.sellerProfile)))
    if product.sellerProfile != user.profile:
        raise HTTPException(status_code=403, detail="You are not the seller of this product")
    
    file_location = f"{UPLOAD_FOLDER}/{product.id}.png"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    product.img = str(file_location)

    await session.commit()
    await session.refresh(product)

    return product


@seller_router.get("/profile/product/image/{id}")
async def get_product_image(id:int, session:AsyncSession = Depends(get_session)):

    product = await session.scalar(select(SellerProduct).where(SellerProduct.id == id))
    if not product:
        raise HTTPException(status_code=404, detail="Product image not found")
    if not product.img:
        raise HTTPException(status_code=404, detail="Product image not found")
    
    file_location = str(product.img)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="Product image not found")
    
    return FileResponse(file_location)