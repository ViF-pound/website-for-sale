import datetime

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

from ..seller.seller_models import Seller, Review

Base = declarative_base()


class User(Base):
    __tablename__ = "users_database"

    id:Mapped[int] = mapped_column(primary_key = True)
    
    name:Mapped[str] 
    email:Mapped[str]
    password:Mapped[bytes]
    dob:Mapped[datetime.date]
    admin:Mapped[str] = "Not admin"
    
    seller_id:Mapped[int] = mapped_column(ForeignKey("sellesr_database.id", ondelete="CASCADE"))
    seller:Mapped["Seller"] = relationship(back_populates="profile", uselist=False)
    reviews:Mapped[list["Review"]] = relationship(back_populates="profile")
