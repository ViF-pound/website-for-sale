from pydantic import BaseModel


class AddProduct(BaseModel):

    produt_id: int


class Review(BaseModel):

    seller_id: int
    estimation: None
    text:str
    