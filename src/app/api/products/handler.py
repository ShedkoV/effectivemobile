from fastapi import Depends, HTTPException, Response, status
from app.api.products.schemas import ProductResponse, ProductRequest


async def get() -> ProductResponse:
    return ProductResponse(
        id=1,
        name='test name',
        description='test description',
        price=1000,
        count=1,
    )


async def get_by_id(
    product_id: int,
) -> ProductResponse:
    return ProductResponse(
        id=1,
        name='test name',
        description='test description',
        price=1000,
        count=1,
    )


async def post(
    request: ProductRequest,
) -> ProductResponse:
    return ProductResponse(
        id=1,
        name=request.name,
        description=request.description,
        price=request.price,
        count=request.count,
    )


async def put(
    product_id: int,
    request: ProductRequest,
) -> ProductResponse:
    return ProductResponse(
        id=product_id,
        name=request.name,
        description=request.description,
        price=request.price,
        count=request.count,
    )


async def delete(
    product_id: int,
) -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
