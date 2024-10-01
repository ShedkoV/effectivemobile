from fastapi import status
import pytest

from app.api.orders.schemas import OrderStatusEnum
from tests.conftest import datetime_now

pytestmark = pytest.mark.anyio


async def test_get(
    test_client,
    product_storage,
    order_storage
):
    expected_value = [
        {
            'status': 'in_process',
            'description': datetime_now,
            'id': 1,
            'items': [
                {'product_id': 1, 'quantity': 5}
            ],
        }
    ]
    response = await test_client.get('/orders/')
    assert response.status_code == status.HTTP_200_OK
    raise ValueError(
        response.json(),
        expected_value
    )
    assert response.json() == expected_value


@pytest.mark.parametrize(
    'order_id, expected_value, expected_status',
    [
        pytest.param(
            0,
            {
                'detail': 'Запись с данным id(0) не найдена',
            },
            status.HTTP_404_NOT_FOUND,
            id='no_order_record',
        ),
        pytest.param(
            1,
            {
                'status': 'in_process',
                'created_at': datetime_now,
                'id': 1,
                'items': [
                    {
                        'product_id': 1,
                        'quantity': 5
                    }
                ]
            },
            status.HTTP_200_OK,
            id='has_record_data',
        ),
    ]
)
async def get_by_id(
    order_id,
    expected_value,
    expected_status,
    test_client,
    product_storage,
    order_storage,
):
    response = await test_client.get(f'/orders/{order_id}')
    assert response.status_code == expected_status
    assert response.json() == expected_value


@pytest.mark.parametrize(
    'request_json, expected_value, expected_status',
    pytest.param(
        None,
        {
            'detail': [
                {
                    'type': 'missing',
                    'loc': [
                        'body'
                    ],
                    'msg': 'Field required',
                    'input': None
                }
            ]
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        id='empty_request_json',
    ),
    pytest.param(
        {
            'items': [
                {
                    'product_id': 1,
                    'quantity': 10
                },
            ],
        },
        {
            'status': 'in_process',
            'created_at': datetime_now,
            'id': 1
        },
        status.HTTP_200_OK,
        id='correct_order_record',
    ),
)
async def test_post(
    request_json,
    expected_value,
    expected_status,
    test_client,
):
    response = await test_client.post('/orders/', json=request_json)
    assert response.status_code == expected_status
    assert response.json() == expected_value


@pytest.mark.parametrize(
    'order_id, request_json, expected_value, expected_status',
    pytest.param(
        1112121,
        {
            "status": OrderStatusEnum.POSTED.value,
        },
        {
            "detail": "Запись с данным id(1111) не найдена"
        },
        status.HTTP_404_NOT_FOUND,
        id='id_not_founded',

    ),
    pytest.param(
        1,
        {
            "status": OrderStatusEnum.POSTED.value,
        },
        {
            "status": OrderStatusEnum.POSTED.value,
            "created_at": datetime_now,
            "id": 1,
            "items": [
                {
                    "product_id": 1,
                    "quantity": 5
                }
            ]
        },
        status.HTTP_200_OK,
        id='edited_record',
    ),
)
async def patch(
    order_id,
    request_json,
    expected_value,
    expected_status,
    order_storage,
    test_client,
):
    response = await test_client.patch(
        f'/orders/{order_id}/status/',
        json=request_json
    )
    assert response.status_code == expected_status
    assert response.json() == expected_value
