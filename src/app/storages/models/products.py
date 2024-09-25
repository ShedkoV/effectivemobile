from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.storages.models.base_model import BaseOrm


class ProductOrm(BaseOrm):
    __tablename__ = 'products'

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped[list['OrderOrm']] = relationship(
        secondary='order_items',
        back_populates="product",
    )
    order_items: Mapped[list['OrderItemOrm']] = relationship(back_populates='product')
