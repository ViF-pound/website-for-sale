from pydantic import BaseModel


class NewCategory(BaseModel):

    name: str


class NewSubcategory(BaseModel):

    category_id: int
    name: str


class NewProduct(BaseModel):

    subcategory_id: int
    name: str