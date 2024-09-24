import enum
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.storages.models.base_model import BaseOrm


class OrderStatus(enum.Enum):
    in_process = 'in_process'
    posted = 'posted'
    delivered = 'delivered'


class OrderOrm(BaseOrm):
    __tablename__ = 'orders'

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[OrderStatus]

    order_items = relationship("OrderItemOrm", back_populates="order")
