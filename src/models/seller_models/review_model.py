from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

if TYPE_CHECKING:
    from seller_model import Seller


class Review(Base):
    __tablename__ = "reviews_seller_table"

    id:Mapped[int] = mapped_column(primary_key = True)

    estimation:Mapped[int] = None
    text:Mapped[str]

    user_id:Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    seller_id:Mapped[int] = mapped_column(ForeignKey("sellers_table.id", ondelete="CASCADE"))
    seller:Mapped["Seller"] = relationship(back_populates="reviews", uselist=False)