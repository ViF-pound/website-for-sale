from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

if TYPE_CHECKING:
    from src.app_auth.auth_models import User
    from src.types.currencyType import CurrencyType
    from src.catalog.catalog_models import Product


class Seller(Base):
    __tablename__ = "sellers_table"

    id:Mapped[int] = mapped_column(primary_key = True)

    rating:Mapped[float]

    user_id:Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete="CASCADE"))
    user:Mapped["User"] = relationship(back_populates="profile", uselist=False)
    reveiws:Mapped[list["Review"]] = relationship(back_populates="seller_reviews", uselist=True)
    products:Mapped[list["Product"]] = relationship(back_populates="seller_products", uselist=True)


class Review(Base):
    __tablename__ = "reviews_seller_table"

    id:Mapped[int] = mapped_column(primary_key = True)

    estimation:Mapped[int] = None
    text:Mapped[str]

    seller_id:Mapped[int] = mapped_column(ForeignKey("sellers_table.id", ondelete="CASCADE"))
    seller:Mapped["Seller"] = relationship(back_populates="reviews", uselist=False)
    user_id:Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete="CASCADE"))
    user:Mapped["User"] = relationship(back_populates="profile", uselist=False)


class SellerProduct(Base):
    __tablename__ = "products_seller_table"

    id:Mapped[int] = mapped_column(primary_key = True)

    name:Mapped[str]
    description:Mapped[str]
    price:Mapped[float]
    currency:Mapped[CurrencyType] = mapped_column(default=CurrencyType.RUB)

    seller_id:Mapped[int] = mapped_column(ForeignKey("sellers_table.id", ondelete="CASCADE"))
    seller:Mapped["Seller"] = relationship(back_populates="products", uselist=False)
    product_id:Mapped[int] = mapped_column(ForeignKey("products_table.id", ondelete="CASCADE"))
    product:Mapped["Product"] = relationship(back_populates="sellers_products", uselist=False)
