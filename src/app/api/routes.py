from fastapi import APIRouter, FastAPI

from app.api.products.handler import (
    get as get_all_products,
    get_by_id as get_product_by_id,
    post as create_new_product,
    put as update_product_by_id,
    delete as delete_product_by_id,
)
from app.api.products.schemas import ProductResponse


def setup_routes(app: FastAPI):
    """Setting up routers."""
    api_products_router = APIRouter(prefix='/products', tags=['Products'])
    api_products_router.api_route(
        path='/',
        methods=['GET'],
        response_model=ProductResponse,
    )(get_all_products)

    api_products_router.api_route(
        path='/{product_id}',
        methods=['GET'],
        response_model=ProductResponse,
    )(get_product_by_id)

    api_products_router.api_route(
        path='/',
        methods=['POST'],
        response_model=ProductResponse,
    )(create_new_product)

    api_products_router.api_route(
        path='/{product_id}',
        methods=['PUT'],
        response_model=ProductResponse,
    )(update_product_by_id)

    api_products_router.api_route(
        path='/{product_id}',
        methods=['DELETE'],
        response_model=ProductResponse,
    )(delete_product_by_id)

    app.include_router(api_products_router)
