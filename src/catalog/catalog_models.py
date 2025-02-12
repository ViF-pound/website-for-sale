from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

if TYPE_CHECKING:
    from src.seller.seller_models import SellerProduct


class Category(Base):
    __tablename__ = "categories_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]

    subcategories:Mapped[list["SubCategory"]] = relationship(back_populates="category", uselist=True)


class SubCategory(Base):
    __tablename__ = "subcategories_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]

    category_id:Mapped[int] = mapped_column(ForeignKey("categories_table.id", ondelete="CASCADE"))
    category:Mapped["Category"] = relationship(back_populates="subcategories", uselist=False)
    products:Mapped[list["Product"]] = relationship(back_populates="subcategory", uselist=True)


class Product(Base):
    __tablename__ = "products_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]

    subcategory_id:Mapped[int] = mapped_column(ForeignKey("subcategories_table.id", ondelete="CASCADE"))
    subcategory:Mapped["SubCategory"] = relationship(back_populates="products", uselist=False)
    sellerproducts:Mapped[list["SellerProduct"]] = relationship(back_populates="product", uselist=True)
    