from http import HTTPStatus

import pytest


def test_get_orders(test_client):
    response = test_client.get('/orders/')
    assert response.status_code == HTTPStatus.OK


def test_get_order_by_id(test_client):
    response = test_client.get('/orders/1')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'request_data, expected_status',
    [
        pytest.param(
            {
                "name": "Iphone 15 pro max",
                "description": "mobile phone",
                "price": 3800,
                "quantity": 150
            },
            HTTPStatus.CREATED,
            id='good_request',
        ),
        pytest.param(
            {},
            HTTPStatus.UNPROCESSABLE_ENTITY,
            id='with_empty_data',
        ),
    ],
)
def test_create_order(
    test_client,
    request_data,
    expected_status,
):
    resp = test_client.post(
        '/orders',
        json=request_data,
    )
    assert resp.status_code == expected_status


def test_delete_product_by_id(test_client):
    resp = test_client.patch('/products/1/status')
    assert resp.status_code == HTTPStatus.OK
