from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storages.models.base_model import BaseOrm


class ProductOrm(BaseOrm):
    __tablename__ = 'products'

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order_items = relationship("OrderItemOrm", back_populates="product")
