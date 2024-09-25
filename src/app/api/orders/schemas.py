from enum import Enum
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderStatusEnum(str, Enum):
    IN_PROCESS = 'in_process'
    POSTED = 'posted'
    DELIVERED = 'delivered'


class OrderItem(BaseModel):
    product_id: int = Field(
        ...,
        description='ID продукта'
    )
    quantity: int = Field(
        ...,
        description='Количество на складе',
    )


class OrderRequest(BaseModel):
    """..."""

    items: list[OrderItem] = Field(
        description='Элементы заказа',
    )


class OrderRecord(BaseModel):
    created_at: Optional[datetime] = Field(
        ...,
        description='Дата заказа',
    )
    status: OrderStatusEnum = Field(
        ...,
        description='Статус заказа',
    )

    class Config:
        """Orm mode on."""
        from_attributes = True


class OrderCreateResponse(OrderRecord):
    id: int = Field(
        ...,
        description='Уникальный номер',
    )


class OrderResponse(OrderRecord):
    id: int = Field(
        ...,
        description='Уникальный номер',
    )
    items: list[OrderItem] = Field(
        description='Элементы заказа',
    )
