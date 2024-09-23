from fastapi import APIRouter, FastAPI

from app.api.products.handler import get as get_all_products
from app.api.products.schemas import ProductResponse


def setup_routes(app: FastAPI):
    """Setting up routers."""
    api_products_router = APIRouter(prefix='/products', tags=['Products'])
    api_products_router.api_route(
        path='/',
        methods=['GET'],
        response_model=ProductResponse,
    )(get_all_products)

    app.include_router(api_products_router)
