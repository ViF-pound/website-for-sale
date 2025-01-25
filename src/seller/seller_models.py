from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

from ..app_auth.auth_models import User
from ..types.currencyType import CurrencyType
from ..catalog.catalog_models import Product

Base = declarative_base()


class Seller(Base):
    __tablename__ = "sellers_database"

    id:Mapped[int] = mapped_column(primary_key = True)

    user_id:Mapped[int] = mapped_column(ForeignKey("users_database.id", ondelete="CASCADE"))
    user:Mapped["User"] = relationship(back_populates="profile", uselist=False)
    reveiws:Mapped[list["Review"]] = relationship(back_populates="seller_reviews",)
    products:Mapped[list["Product"]] = relationship(back_populates="seller_products", uselist=False)


class Review(Base):
    __tablename__ = "reviews_seller_database"

    id:Mapped[int] = mapped_column(primary_key = True)

    estimation:Mapped[float] = None
    text:Mapped[str]

    seller_id:Mapped[int] = mapped_column(ForeignKey("sellers_database.id", ondelete="CASCADE"))
    seller:Mapped["Seller"] = relationship(back_populates="reviews")
    user_id:Mapped[int] = mapped_column(ForeignKey("users_database.id", ondelete="CASCADE"))
    user:Mapped["User"] = relationship(back_populates="profile")


class SellerProduct(Base):
    __tablename__ = "products_seller_database"

    id:Mapped[int] = mapped_column(primary_key = True)

    name:Mapped[str]
    descrition:Mapped[str]
    price:Mapped[float]
    currency:Mapped[CurrencyType] = mapped_column(default=CurrencyType.RUB)

    seller_id:Mapped[int] = mapped_column(ForeignKey("sellers_database.id", ondelete="CASCADE"))
    seller:Mapped["Seller"] = relationship(back_populates="products")
    product_id:Mapped[int] = mapped_column(ForeignKey("products_database.id", ondelete="CASCADE"))
    product:Mapped["Product"] = relationship(back_populates="seller_products")
