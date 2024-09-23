from app.api.orders.schemas import OrderResponse, OrderRequest, OrderStatusEnum


async def post(
    request: OrderRequest,
) -> OrderResponse:
    return OrderResponse(
        id=1,
        status=OrderStatusEnum.POSTED,
    )


async def get() -> OrderResponse:
    return OrderResponse(
        id=1,
        status=OrderStatusEnum.POSTED,
    )


async def get_by_id(
    order_id: int,
) -> OrderResponse:
    return OrderResponse(
        id=order_id,
        status=OrderStatusEnum.POSTED,
    )


async def patch(
    order_id: int,
) -> OrderResponse:
    return OrderResponse(
        id=order_id,
        status=OrderStatusEnum.POSTED,
    )
