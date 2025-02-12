from pydantic import BaseModel


class AddProduct(BaseModel):

    produt_id: int
    