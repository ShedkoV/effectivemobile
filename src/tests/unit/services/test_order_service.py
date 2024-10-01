from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.api.orders.schemas import OrderItem, OrderResponse, OrderStatusEnum
from app.services.order_service import OrderService
from tests.factories.models import OrderItemOrmFactory, OrderOrmFactory

DATE_NOW = datetime.utcnow()


@pytest.mark.parametrize('order_data, expected_result')(
    [
        pytest.param(
            [],
            [],
            id='empty_order_data',
        ),
        pytest.param(
            [
                OrderOrmFactory(
                    id=1,
                    created_at=DATE_NOW,
                    status=OrderStatusEnum.IN_PROCESS,
                    product_items=[
                        OrderItemOrmFactory(
                            id=1,
                            product_id=1,
                            quantity=1,
                        ),
                    ]
                ),
            ],
            [
                OrderResponse(
                    created_at=DATE_NOW,
                    status=OrderStatusEnum.IN_PROCESS,
                    id=1,
                    items=[
                        OrderItem(
                            product_id=1,
                            quantity=1,
                        )
                    ],
                ),
            ],
            id='has_order_data',
        ),
    ]
)
async def test_order_service__get_all(
    order_data,
    expected_result,
):
    mock_session = AsyncMock()
    order_service = OrderService(session=mock_session)
    order_service._get_orders = AsyncMock(return_value=order_data)

    result = await order_service.get_all()
    assert result == expected_result


@pytest.mark.parametrize('order_id, order_data, expected_result')(
    [
        pytest.param(
            None,
            None,
            None,
            id='id_is_none',
        ),
        pytest.param(
            1,
            None,
            None,
            id='empty_order_data_by_id',
        ),
        pytest.param(
            OrderOrmFactory(
                id=1,
                created_at=DATE_NOW,
                status=OrderStatusEnum.IN_PROCESS,
                product_items=[
                    OrderItemOrmFactory(
                        id=1,
                        product_id=1,
                        quantity=1,
                    ),
                ]
            ),
            OrderResponse(
                created_at=DATE_NOW,
                status=OrderStatusEnum.IN_PROCESS,
                id=1,
                items=[
                    OrderItem(
                        product_id=1,
                        quantity=1,
                    )
                ],
            ),
            id='has_order_data_by_id',
        ),
    ]
)
async def test_order_service__get_by_id(
    order_id,
    order_data,
    expected_result,
):
    mock_session = AsyncMock()
    order_service = OrderService(session=mock_session)
    order_service._get_order_by_id = AsyncMock(return_value=order_data)

    result = await order_service.get_by_id(order_id)
    assert result == expected_result
