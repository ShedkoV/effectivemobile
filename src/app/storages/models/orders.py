import enum
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storages.models.base_model import BaseOrm


class OrderStatus(enum.Enum):
    """Перечисление статусов закзов."""

    in_process = 'in_process'
    posted = 'posted'
    delivered = 'delivered'


class OrderOrm(BaseOrm):
    """Модель записи заказа."""

    __tablename__ = 'orders'

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[OrderStatus]

    product: Mapped[list['ProductOrm']] = relationship(
        secondary='order_items',
        back_populates='order',
    )

    product_items: Mapped[list['OrderItemOrm']] = relationship(back_populates='order')
