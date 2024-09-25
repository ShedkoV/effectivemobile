from fastapi import APIRouter, FastAPI

from app.api.orders.schemas import OrderResponse, OrderCreateResponse
from app.api.orders.handler import (
    get as get_all_orders,
    get_by_id as get_order_by_id,
    post as create_new_order,
    patch as updated_order_status_by_id,
)
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
        response_model=list[ProductResponse],
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

    api_orders_router = APIRouter(prefix='/orders', tags=['Orders'])
    api_orders_router.api_route(
        path='/',
        methods=['POST'],
        response_model=OrderCreateResponse,
    )(create_new_order)

    api_orders_router.api_route(
        path='/',
        methods=['GET'],
        response_model=list[OrderResponse],
    )(get_all_orders)

    api_orders_router.api_route(
        path='/{order_id}',
        methods=['GET'],
        response_model=OrderResponse,
    )(get_order_by_id)

    api_orders_router.api_route(
        path='/{order_id}/status',
        methods=['PATCH'],
        response_model=OrderResponse,
    )(updated_order_status_by_id)

    app.include_router(api_products_router)
    app.include_router(api_orders_router)
