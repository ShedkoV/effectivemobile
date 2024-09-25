from typing import Annotated

from fastapi import Depends

from app.api.orders.schemas import OrderRequest, OrderResponse
from app.services.order_service import OrderService


async def post(
    request: OrderRequest,
    service: Annotated[OrderService, Depends()],
) -> list[OrderResponse]:
    return await service.create(request)


async def get(service: Annotated[OrderService, Depends()]) -> OrderResponse:
    return await service.get_all_items()


async def get_by_id(
    order_id: int,
    service: Annotated[OrderService, Depends()],
) -> OrderResponse:
    return await service.get_item(order_id)


async def patch(
    order_id: int,
    request: OrderRequest,
    service: Annotated[OrderService, Depends()],
) -> OrderResponse:
    return await service.update_status(
        order_id=order_id,
        request=request,
    )
