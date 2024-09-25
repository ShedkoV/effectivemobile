from enum import Enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderStatusEnum(str, Enum):
    """Перечисление статусов закзов."""
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


class BaseOrder(BaseModel):
    """Базовый класс для запроса заказа в сервис и его ответа."""

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


class OrderRequest(BaseOrder):
    """Запрос на создание заказа."""


class OrderCreateResponse(OrderRecord):
    id: int = Field(
        ...,
        description='Уникальный номер',
    )


class OrderResponse(BaseOrder):
    """Ответ принятого заказаю."""

    id: int = Field(
        ...,
        description='Уникальный номер',
    )
    items: list[OrderItem] = Field(
        description='Элементы заказа',
    )
