from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship

from src.db import Base

if TYPE_CHECKING:
    from src.models.seller_models.sellerProduct_model import SellerProduct
    from src.models.user_model import User


class UserBacket(Base):
    __tablename__ = "backet_user_table"

    counts:Mapped[int] = mapped_column(default=1)

    user_id:Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete="CASCADE"), primary_key=True)
    user:Mapped["User"] = relationship(uselist=False)

    product_id:Mapped[int] = mapped_column(ForeignKey("products_seller_table.id", ondelete="CASCADE"), primary_key=True)
    product:Mapped["SellerProduct"] = relationship(uselist=False)
