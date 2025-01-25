from pydantic import BaseModel

from ..types.currencyType import CurrencyType

class Product(BaseModel):

    name:str
    description:str
    price:float
    currency:CurrencyType

class Review(BaseModel):

    estimation:float
    text:str
