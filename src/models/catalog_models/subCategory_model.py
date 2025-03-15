from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

if TYPE_CHECKING:
    from category_model import Category
    from product_model import Product


class SubCategory(Base):
    __tablename__ = "subcategories_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]

    category_id:Mapped[int] = mapped_column(ForeignKey("categories_table.id", ondelete="CASCADE"))
    category:Mapped["Category"] = relationship(back_populates="subcategories", uselist=False)
    products:Mapped[list["Product"]] = relationship(back_populates="subcategory", uselist=True)