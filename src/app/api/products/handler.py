from app.api.products.schemas import ProductResponse


async def get() -> ProductResponse:
    return ProductResponse(
        id=1,
        name='test name',
        description='test description',
        price=1000,
        count=1,
    )