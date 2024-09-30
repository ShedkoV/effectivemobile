from fastapi import status
import pytest


pytestmark = pytest.mark.anyio


async def test_get_products(test_client, product_storage):
    expected_value = [
        {
            'name': 'Iphone 15 pro max',
            'description': 'Mobile phone',
            'price': 3100.0,
            'quantity': 100,
            'id': 1,
        }
    ]
    response = await test_client.get('/products/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_value


@pytest.mark.parametrize(
    'product_id, expected_value, expected_status',
    [
        pytest.param(
            0,
            {
                'detail': 'Запись с данным id(0) не найдена',
            },
            status.HTTP_404_NOT_FOUND,
            id='no_product_record',
        ),
        pytest.param(
            1,
            {
                'name': 'Iphone 15 pro max',
                'description': 'Mobile phone',
                'price': 3100.0,
                'quantity': 100,
                'id': 1,
            },
            status.HTTP_200_OK,
            id='has_product_data',
        ),
    ]
)
async def test_get_product_by_id(
    product_id,
    expected_value,
    expected_status,
    test_client,
    product_storage,
):
    response = await test_client.get(f'/products/{product_id}')
    assert response.status_code == expected_status
    assert response.json() == expected_value
