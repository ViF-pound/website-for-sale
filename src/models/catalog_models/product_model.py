from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

if TYPE_CHECKING:
    from subCategory_model import SubCategory
    from src.models.seller_models.sellerProduct_model import SellerProduct


class Product(Base):
    __tablename__ = "products_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]

    subcategory_id:Mapped[int] = mapped_column(ForeignKey("subcategories_table.id", ondelete="CASCADE"))
    subcategory:Mapped["SubCategory"] = relationship(back_populates="products", uselist=False)
    seller_products:Mapped[list["SellerProduct"]] = relationship(back_populates="product", uselist=True)
    