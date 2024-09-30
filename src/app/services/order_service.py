from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.orders.schemas import OrderItem, OrderRequest, OrderResponse, OrderStatusEnum
from app.services.base_service import BaseService
from app.services.product_service import ProductService
from app.storages.database import get_async_session
from app.storages.models import OrderItemOrm
from app.storages.models.orders import OrderOrm


class OrderService(BaseService):
    """Класс, для операций на эндпоинтах /orders."""

    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_async_session)],
    ) -> None:
        super().__init__(session, OrderOrm)
        self._product_service = ProductService(session=session)
        self._relation_field = OrderOrm.product_items

    async def get_all(self) -> list[OrderResponse]:
        """Получить все заказы."""
        orders = await self.get_all_items()

        response = []
        for order in orders:
            items = [
                OrderItem(product_id=item.product_id, quantity=item.quantity)
                for item in order.product_items
            ]
            response.append(
                OrderResponse(
                    created_at=order.created_at,
                    status=order.status.value,
                    id=order.id,
                    items=items,
                ),
            )

        return response

    async def get_by_id(self, order_id: int) -> OrderResponse:
        """Получить заказ по его id."""
        order = await self.get_item(order_id)
        items = [
            OrderItem(product_id=item.product_id, quantity=item.quantity)
            for item in order.product_items
        ]

        return OrderResponse(
            created_at=order.created_at,
            status=order.status.value,
            id=order.id,
            items=items,
        )

    async def create_order(self, request: OrderRequest) -> OrderOrm:
        """Создать новй заказ."""
        await self._validate_items(request.items)

        new_order = OrderOrm(
            created_at=datetime.utcnow(),
            status=OrderStatusEnum.IN_PROCESS.value,
        )

        self._session.add(new_order)
        await self._session.commit()
        await self._session.refresh(new_order)
        await self._create_order_items(new_order, request.items)

        return new_order

    async def update_status(self, order_id: int, request: OrderRequest) -> OrderOrm:
        """Обновление статуса заказа по его id."""
        order = await self.get_item(order_id)
        order.status = request.status
        await self._session.commit()
        await self._session.refresh(order)

        return order

    async def _validate_items(self, items: list[OrderRequest]) -> None:
        """Проверяет наличие и количество товара для каждого элемента заказа."""
        for item in items:
            product = await self._product_service.get_item(item.product_id)
            if not product or product.quantity < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Недостаточное кол-во товара: {product.name}',
                )

    async def _create_order_items(
        self,
        order: OrderOrm,
        items: list[OrderRequest],
    ) -> None:
        """Создает элементы заказа."""
        for item in items:
            product = await self._product_service.get_item(item.product_id)
            product.quantity -= item.quantity
            self._session.add(product)

            order_item = OrderItemOrm(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
            )
            self._session.add(order_item)

        await self._session.commit()
