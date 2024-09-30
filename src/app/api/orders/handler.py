from typing import Annotated

from fastapi import Depends

from app.api.orders.schemas import OrderCreateResponse, OrderRequest, OrderResponse, OrderStatus
from app.services.order_service import OrderService


async def post(
    request: OrderRequest,
    service: Annotated[OrderService, Depends()],
) -> OrderCreateResponse:
    """Оформить новый заказ."""
    return await service.create_order(request)


async def get(service: Annotated[OrderService, Depends()]) -> OrderResponse:
    """Получить информацию о всех заказах."""
    return await service.get_all()


async def get_by_id(
    order_id: int,
    service: Annotated[OrderService, Depends()],
) -> OrderResponse:
    """Получить информацию о заказе по его id."""
    return await service.get_by_id(order_id)


async def patch(
    order_id: int,
    request: OrderStatus,
    service: Annotated[OrderService, Depends()],
) -> OrderResponse:
    """Обновить статус существующего заказа."""
    return await service.update_status(
        order_id=order_id,
        request=request,
    )
