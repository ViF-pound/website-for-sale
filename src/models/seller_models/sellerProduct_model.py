from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

from src.types.currencyType import CurrencyType

if TYPE_CHECKING:
    from src.models.catalog_models.product_model import Product
    from src.models.seller_models.seller_model import Seller
    from src.models.user_model import User


class SellerProduct(Base):
    __tablename__ = "products_seller_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]
    description:Mapped[str]
    price:Mapped[float]
    currency:Mapped[CurrencyType] = mapped_column(default=CurrencyType.RUB)

    seller_id:Mapped[int] = mapped_column(ForeignKey("sellers_table.id", ondelete="CASCADE"))
    seller:Mapped["Seller"] = relationship(back_populates="products", uselist=False)

    product_id:Mapped[int] = mapped_column(ForeignKey("products_table.id", ondelete="CASCADE"))
    product:Mapped["Product"] = relationship(back_populates="seller_products", uselist=False)

    backets:Mapped[list["User"]] = relationship(secondary="backet_user_table", back_populates="backet", uselist=True)
