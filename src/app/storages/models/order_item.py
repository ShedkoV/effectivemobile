from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.storages.models.base_model import Base


class OrderItem(Base):
    __tablename__ = 'order_items'

    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
