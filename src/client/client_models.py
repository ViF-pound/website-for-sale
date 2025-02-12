from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship

from src.db import Base

if TYPE_CHECKING:
    from src.seller.seller_models import SellerProduct
    from src.app_auth.auth_models import User


class UserBacket(Base):
    __tablename__ = "backet_user_table"

    id:Mapped

    user_id:Mapped[int] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"))
    user:Mapped["User"] = relationship(back_populates="backet", uselist=False)

    product_id:Mapped[int] = mapped_column(ForeignKey("sellet_product.id", ondelete="CASCADE"))
    product:Mapped["SellerProduct"] = relationship(uselist=False)