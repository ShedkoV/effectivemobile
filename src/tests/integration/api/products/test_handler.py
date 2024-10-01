from fastapi import status
import pytest


pytestmark = pytest.mark.anyio


async def test_get(test_client, product_storage):
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
async def test_get_by_id(
    product_id,
    expected_value,
    expected_status,
    test_client,
    product_storage,
):
    response = await test_client.get(f'/products/{product_id}')
    assert response.status_code == expected_status
    assert response.json() == expected_value


@pytest.mark.parametrize(
    'request_json, expected_value, expected_status',
    [
        pytest.param(
            None,
            {'detail':[{'type':'missing','loc':['body'],'msg':'Field required','input':None}]},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='empty_request_body',
        ),
        pytest.param(
            {
                'name': 15,
                'description': 'mobile phone',
                'price': 1500,
                'quantity': 100
            },
            {
                'detail': [
                    {'type': 'string_type', 'loc': ['body', 'name'], 'msg': 'Input should be a valid string', 'input': 15}
                ]
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            id='request_body_with_invalid_field',
        ),
        pytest.param(
            {
                'name': 'Iphone 25 pro max',
                'description': 'mobile phone',
                'price': 1500,
                'quantity': 100,
            },
            {
                'name': 'Iphone 25 pro max',
                'description': 'mobile phone',
                'price': 1500,
                'quantity': 100,
                'id': 1,
            },
            status.HTTP_200_OK,
            id='created_new_product',
        ),
    ]
)
async def test_post(
    request_json,
    expected_value,
    expected_status,
    test_client,
):
    response = await test_client.post('/products/', json=request_json)
    assert response.status_code == expected_status
    assert response.json() == expected_value


@pytest.mark.parametrize(
    'product_id, request_json, expected_value, expected_status',
    [
        pytest.param(
            11212,
            {
                'name': 'Iphone 12 pro',
                'description': 'mobile phone',
                'price': 1000,
                'quantity': 10,
            },
            {
                'detail': 'Запись с данным id(1212) не найдена',
            },
            status.HTTP_200_OK,
            id='ivalid_id_product_record'
        ),
        pytest.param(
            1,
            {
                'name': 'Iphone 12 pro',
                'description': 'mobile phone',
                'price': 1000,
                'quantity': 10,
            },
            {
                'name': 'Iphone 12 pro',
                'description': 'mobile phone',
                'price': 1000,
                'quantity': 10,
                'id': 1
            },
            status.HTTP_404_NOT_FOUND,
            id='edited_product_data'
        ),
    ]
)
async def put(
    product_id,
    request_json,
    expected_status,
    expected_value,
    product_storage,
    test_client,
):
    response = await test_client.put(f'/products/{product_id}', json=request_json)
    assert response.status_code == expected_status
    assert response.json() == expected_value
