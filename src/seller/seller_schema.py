from pydantic import BaseModel

from src.types.currencyType import CurrencyType


class NewProduct(BaseModel):

    name: str
    description: str
    price: float
    currency: CurrencyType
    product_id: int

