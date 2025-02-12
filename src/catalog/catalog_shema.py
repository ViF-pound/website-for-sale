from pydantic import BaseModel


class NewCategory(BaseModel):

    new_category: str


class NewSubcategory(BaseModel):

    id_category: int
    new_subcategory: str


class NewProduct(BaseModel):

    id_subcategory: int
    new_product: str