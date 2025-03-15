import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship

from typing import TYPE_CHECKING

from src.db import Base

if TYPE_CHECKING:
    from src.models.seller_models.seller_model import Seller
    from src.models.seller_models.sellerProduct_model import SellerProduct


class User(Base):
    __tablename__ = "users_table"

    id:Mapped[int] = mapped_column(primary_key=True)
    
    profile_name:Mapped[str]
    user_name:Mapped[str] = mapped_column(unique=True)
    email:Mapped[str] = mapped_column(unique=True)
    password:Mapped[bytes]
    dob:Mapped[datetime.date]
    admin:Mapped[str] = mapped_column(default=False)
    
    seller_id:Mapped[int] = mapped_column(ForeignKey("sellers_table.id"), nullable=True)
    seller:Mapped["Seller"] = relationship(back_populates="user", uselist=False)

    backet:Mapped[list["SellerProduct"]] = relationship(secondary="backet_user_table", back_populates="backets", uselist=True)