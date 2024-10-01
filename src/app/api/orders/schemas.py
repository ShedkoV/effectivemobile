from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class OrderStatusEnum(str, Enum):
    """Перечисление статусов закзов."""

    IN_PROCESS = 'in_process'
    POSTED = 'posted'
    DELIVERED = 'delivered'


class OrderItem(BaseModel):
    """Элемент заказа."""

    product_id: int = Field(
        ...,
        description='ID продукта',
    )
    quantity: int = Field(
        ...,
        description='Количество на складе',
    )


class OrderRequest(BaseModel):
    """Базовый класс для запроса заказа в сервис и его ответа."""

    items: list[OrderItem] = Field(
        description='Элементы заказа',
    )


class OrderStatus(BaseModel):
    """Класс для обновления статуса заказа."""

    status: OrderStatusEnum = Field(
        ...,
        description='Статус заказа',
    )


class OrderRecord(OrderStatus):
    """Запрос на создание заказа."""

    created_at: Optional[datetime] = Field(
        ...,
        description='Дата заказа',
    )

    class Config:
        """Orm mode on."""

        from_attributes = True


class OrderCreateResponse(OrderRecord):
    """Ответ оформленного заказа."""

    id: int = Field(
        ...,
        description='Уникальный номер',
    )


class OrderResponse(OrderRecord):
    """Ответ принятого заказаю."""

    id: int = Field(
        ...,
        description='Уникальный номер',
    )
    items: list[OrderItem] = Field(
        description='Элементы заказа',
    )
