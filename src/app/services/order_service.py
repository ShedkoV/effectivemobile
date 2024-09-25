from datetime import datetime
from typing import Annotated

from fastapi import Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.orders.schemas import OrderRequest, OrderStatusEnum, OrderResponse, OrderItem
from app.services.base_service import BaseService
from app.services.product_service import ProductService
from app.storages.database import get_session
from app.storages.models import OrderItemOrm
from app.storages.models.orders import OrderOrm


class OrderService(BaseService):
    """Класс, для операций на эндпоинтах /orders"""

    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> None:
        super().__init__(session, OrderOrm)
        self._product_service = ProductService(session=session)

    async def get_all(self) -> OrderResponse:
        result = await self._session.execute(
            select(OrderOrm).options(selectinload(OrderOrm.product_items))
        )
        orders = result.scalars().all()

        response = []
        for order in orders:
            items = [
                OrderItem(product_id=item.product_id, quantity=item.quantity)
                for item in order.product_items
            ]
            response.append(
                OrderResponse(created_at=order.created_at, status=order.status.value, id=order.id, items=items))

        return response

    async def get_by_id(self, order_id):
        result = await self._session.execute(
            select(OrderOrm).options(selectinload(OrderOrm.product_items)).filter(OrderOrm.id == order_id)
        )
        order = result.scalar_one_or_none()
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")

        items = [
            OrderItem(product_id=item.product_id, quantity=item.quantity)
            for item in order.product_items
        ]

        return OrderResponse(created_at=order.created_at, status=order.status.value, id=order.id, items=items)

    async def create_order(self, request: OrderRequest) -> OrderOrm:
        items = request.items
        for item in items:
            product = await self._product_service.get_item(item.product_id)
            if not product or product.quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f'Недостаточное кол-во товара: {product.name}',
                )

            new_order = OrderOrm(
                created_at=datetime.utcnow(),
                status=OrderStatusEnum.IN_PROCESS.value,
            )
            self._session.add(new_order)
            await self._session.commit()
            await self._session.refresh(new_order)

            product.quantity -= item.quantity
            self._session.add(product)
            await self._session.commit()

            order_item = OrderItemOrm(order_id=new_order.id, product_id=product.id, quantity=product.quantity)
            self._session.add(order_item)
            await self._session.commit()

            return new_order

    async def update_status(self, order_id: int, request: OrderRequest) -> OrderOrm:
        """Обновление статуса заказа по его id."""
        order = await self.get_item(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        order.status = request.status
        await self._session.commit()
        await self._session.refresh(order)

        return order
