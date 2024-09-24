from typing import Annotated

from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.orders.schemas import OrderRequest
from app.services.base_service import BaseService
from app.storages.database import get_session
from app.storages.models.orders import OrderOrm


class OrderService(BaseService):

    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> None:
        super().__init__(session, OrderOrm)

    async def update_status(self, order_id: int, request: OrderRequest) -> OrderOrm:
        order = await self.get_item(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        order.status = request.status
        await self._session.commit()
        await self._session.refresh(order)

        return order
