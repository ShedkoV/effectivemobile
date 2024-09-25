from typing import Annotated

from fastapi import Depends, HTTPException, Response, status

from app.api.products.schemas import ProductRequest, ProductResponse
from app.services.product_service import ProductService


async def get(
    service: Annotated[ProductService, Depends()],
) -> list[ProductResponse]:
    """Get all content records."""
    return await service.get_all_items()


async def get_by_id(
    product_id: int,
    service: Annotated[ProductService, Depends()],
) -> ProductResponse:
    """Получить продукт по его id."""
    return await service.get_item(product_id)


async def post(
    request: ProductRequest,
    service: Annotated[ProductService, Depends()],
) -> ProductResponse:
    """Создать новый продукт."""
    return await service.create(request)


async def put(
    product_id: int,
    request: ProductRequest,
    service: Annotated[ProductService, Depends()],
) -> ProductResponse:
    """Обнвить продукт по его id."""
    return await service.update(
        obj_id=product_id,
        request=request,
    )


async def delete(
    product_id: int,
    service: Annotated[ProductService, Depends()],
) -> Response:
    """Delete record by id."""
    if not await service.delete(product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
