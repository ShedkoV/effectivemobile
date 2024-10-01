from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.products.schemas import ProductRequest
from app.services.base_service import BaseService
from app.storages.database import get_async_session
from app.storages.models import ProductOrm


class ProductService(BaseService):
    """Класс, для операций на эндпоинтах /orders."""

    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_async_session)],
    ) -> None:
        super().__init__(session, ProductOrm)
        self._relation_field = ProductOrm.order_items

    async def create(self, request: ProductRequest) -> ProductOrm:
        """Создает навую модель продукта в БД."""
        async with self._session.begin():
            operation = self._model(**request.dict())
            self._session.add(operation)
            await self._session.commit()
        await self._session.refresh(operation)

        return operation
