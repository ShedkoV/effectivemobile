from enum import Enum
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class OrderStatusEnum(str, Enum):
    IN_PROCESS = 'in_process'
    POSTED = 'posted'
    DELIVERED = 'delivered'


class BaseOrder(BaseModel):
    """..."""

    created_at: Optional[date] = Field(
        description='Дата заказа',
    )
    status: OrderStatusEnum = Field(
        ...,
        description='Статус заказа',
    )


class OrderRequest(BaseOrder):
    """..."""


class OrderResponse(BaseOrder):
    id: int = Field(
        ...,
        description='Уникальный номер',
    )

    class Config:
        """Orm mode on."""
        from_attributes = True
