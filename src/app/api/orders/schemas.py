from enum import Enum
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class OrderStatusEnum(str, Enum):
    """Перечисление статусов закзов."""
    IN_PROCESS = 'in_process'
    POSTED = 'posted'
    DELIVERED = 'delivered'


class BaseOrder(BaseModel):
    """Базовый класс для запроса заказа в сервис и его ответа."""

    created_at: Optional[date] = Field(
        description='Дата заказа',
    )
    status: OrderStatusEnum = Field(
        ...,
        description='Статус заказа',
    )


class OrderRequest(BaseOrder):
    """Запрос на создание заказа."""


class OrderResponse(BaseOrder):
    """Ответ принятого заказаю."""
    id: int = Field(
        ...,
        description='Уникальный номер',
    )

    class Config:
        """Orm mode on."""
        from_attributes = True
