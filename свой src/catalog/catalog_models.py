from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

from ..seller.seller_models import SellerProduct

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories_database"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]

    subcategories:Mapped[list["SubCategory"]] = relationship(back_populates="category")


class SubCategory(Base):
    __tablename__ = "subcategories_database"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]

    category_id:Mapped[int] = mapped_column(ForeignKey("categories_database.id", ondelete="CASCADE"))
    category:Mapped["Category"] = relationship(back_populates="subcategories")
    products:Mapped[list["Product"]] = relationship(back_populates="subcategory")


class Product(Base):
    __tablename__ = "products_database"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]

    subcategory_id:Mapped[int] = mapped_column(ForeignKey("sibcategories_database.id", ondelete="CASCADE"))
    subcategory:Mapped["SubCategory"] = relationship(back_populates="products")
    sellerproducts:Mapped[list["SellerProduct"]] = relationship(back_populates="product")
    