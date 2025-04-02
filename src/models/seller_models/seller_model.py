from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base
from src.models.seller_models.review_model import Review

if TYPE_CHECKING:
    from src.models.user_model import User
    from src.models.seller_models.sellerProduct_model import SellerProduct


class Seller(Base):
    __tablename__ = "sellers_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    seller_name:Mapped[str] = mapped_column(unique=True)
    rating:Mapped[float] = mapped_column(default=0.00)

    user:Mapped["User"] = relationship(back_populates="seller", uselist=False)
    reviews:Mapped[list["Review"]] = relationship(back_populates="seller", uselist=True)
    products:Mapped[list["SellerProduct"]] = relationship(back_populates="seller", uselist=True)