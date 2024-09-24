from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.storages.models.base_model import BaseOrm


class OrderItemOrm(BaseOrm):
    __tablename__ = 'order_items'

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order = relationship("OrderOrm", back_populates="order_items")
    product = relationship("ProductOrm", back_populates="order_items")

