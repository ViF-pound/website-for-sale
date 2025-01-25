from fastapi import APIRouter

from ..catalog.catalog_models import Category, SubCategory, Product

catalog_router = APIRouter(prefix="/catalog", teg=["catalog"])

@catalog_router.post("/new_category")
async def new_category(name: str):
    NewCategory = Category(name = name)
    session.add(NewCategory)
    await session.commit()
    return "New category add"

@catalog_router.post("/new_subcatalog")
async def new_subcategory(name: str, id: int):
    NewSubcategory = SubCategory(name = name)
    session.add(NewSubcategory)
    await session.commit()
    return "New subcategory add"

@catalog_router.post("/new_product")
async def new_product(name: str):
    NewProduct = Product(name = name)
    session.add(NewProduct)
    await session.commit()
    return "New product add"