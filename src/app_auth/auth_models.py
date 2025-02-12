import datetime

from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship

from src.db import Base

if TYPE_CHECKING:
    from src.seller.seller_models import Review, Seller, SellerProduct


class User(Base):
    __tablename__ = "users_table"

    id:Mapped[int] = mapped_column(primary_key = True)
    
    profile_name:Mapped[str]
    user_name:Mapped[str] = mapped_column(unique=True)
    email:Mapped[str] = mapped_column(unique=True)
    password:Mapped[bytes]
    dob:Mapped[datetime.date]
    admin:Mapped[str] = False
    
    seller_id:Mapped[int] = mapped_column(ForeignKey("sellers_table.id", ondelete="CASCADE"))
    seller:Mapped["Seller"] = relationship(back_populates="profile", uselist=False)
    reviews:Mapped[list["Review"]] = relationship(back_populates="profile", uselist=True)
    products:Mapped[list["SellerProduct"]] = relationship(back_populates="profile", uselist=True)