from pydantic import BaseModel

from src.types.currencyType import CurrencyType


class NewSeller(BaseModel):

    seller_name: str


class NewProduct(BaseModel):

    name: str
    description: str
    price: float
    currency: CurrencyType
    product_id: int

