from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.storages.models.base_model import BaseOrm


class OrderItemOrm(BaseOrm):
    __tablename__ = 'order_items'

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped['OrderOrm'] = relationship(back_populates='product_items')
    product: Mapped['ProductOrm'] = relationship(back_populates='order_items')
