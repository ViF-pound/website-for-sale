from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.catalog_models.category_model import Category
from src.models.catalog_models.subCategory_model import SubCategory
from src.models.catalog_models.product_model import Product
from src.db import get_session
from src.catalog.catalog_schema import NewCategory, NewSubcategory, NewProduct


catalog_router = APIRouter(prefix="/catalog", tags=["catalog"])


@catalog_router.post("/add/category")
async def new_category(data_newcategory: NewCategory, session:AsyncSession = Depends(get_session)):

    NewCategory = Category(name = data_newcategory.name)

    session.add(NewCategory)
    await session.commit()
    await session.refresh(NewCategory)

    return NewCategory


@catalog_router.post("/add/subcatalog")
async def new_subcategory(data_newsubcategory: NewSubcategory, session:AsyncSession = Depends(get_session)):

    category = await session.scalar(select(Category).where(Category.id == data_newsubcategory.category_id))
    if not category:
        raise HTTPException(status_code=404, detail="not found category")
    
    NewSubcategory = SubCategory(**data_newsubcategory.model_dump())

    session.add(NewSubcategory)
    await session.commit()
    await session.refresh(NewSubcategory)

    return NewSubcategory


@catalog_router.post("/add/product")
async def new_product(data_newproduct: NewProduct, session:AsyncSession = Depends(get_session)):

    subCategory = await session.scalar(select(SubCategory).where(SubCategory.id == data_newproduct.subcategory_id))
    if not subCategory:
        raise HTTPException(status_code=404, detail="not found subCategory")

    NewProduct = Product(**data_newproduct.model_dump())

    session.add(NewProduct)
    await session.commit()
    await session.refresh(NewProduct)
    
    return NewProduct