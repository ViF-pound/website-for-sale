from fastapi import APIRouter

from src.catalog.catalog_models import Category, SubCategory, Product
from src.db import session
from src.catalog.catalog_shema import NewCategory, NewSubcategory, NewProduct


catalog_router = APIRouter(prefix="/catalog", tags=["catalog"])


@catalog_router.post("/add/category")
async def new_category(data_newcategory: NewCategory):

    NewCategory = Category(name = data_newcategory.name)

    session.add(NewCategory)
    await session.commit()
    await session.refresh(NewCategory)

    return {"message": "new category add"}


@catalog_router.post("/add/subcatalog")
async def new_subcategory(data_newsubcategory: NewSubcategory):

    NewSubcategory = SubCategory(category_id = data_newsubcategory.category_id, name = data_newsubcategory.name)

    session.add(NewSubcategory)
    await session.commit()
    await session.refresh(NewSubcategory)

    return {"message": "new subcategory add"}


@catalog_router.post("/add/product")
async def new_product(data_newproduct: NewProduct):

    NewProduct = Product(subcategory_id = data_newproduct.subcategory_id, name = data_newproduct.name)

    session.add(NewProduct)
    await session.commit()
    await session.refresh(NewProduct)
    
    return {"message": "new product add"}