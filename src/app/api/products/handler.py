from fastapi import Depends, HTTPException, Response, status
from app.api.products.schemas import ProductResponse, ProductRequest
from app.services.product_service import ProductService


service_dependency = Depends(ProductService)


async def get(
    service: ProductService = service_dependency,
) -> list[ProductResponse]:
    """Get all content records."""
    return await service.get_list_products()


async def get_by_id(
    product_id: int,
    service: ProductService = service_dependency,
) -> ProductResponse:
    return await service.get_item(product_id)


async def post(
    request: ProductRequest,
    service: ProductService = service_dependency,
) -> ProductResponse:
    return await service.create(request)


async def put(
    product_id: int,
    request: ProductRequest,
    service: ProductService = service_dependency,
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
    service: ProductService = service_dependency,
) -> Response:
    """Delete record by id."""
    if not await service.delete(product_id=product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
