from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

if TYPE_CHECKING:
    from subCategory_model import SubCategory


class Category(Base):
    __tablename__ = "categories_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str] = mapped_column()

    subcategories:Mapped[list["SubCategory"]] = relationship(back_populates="category", uselist=True)