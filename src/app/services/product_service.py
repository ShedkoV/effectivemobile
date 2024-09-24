from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.api.products.schemas import ProductRequest
from app.storages.database import get_session, async_session
from app.storages.models import ProductOrm

default_session = Depends(get_session)


class ProductService:

    def __init__(self, session: async_session = default_session) -> None:
        self._session = session

    async def get_list_products(self) -> list[ProductOrm]:
        """Get all products."""
        async with self._session.begin():
            scalar_result = await self._session.scalars(
                select(ProductOrm).order_by(ProductOrm.id),
            )
            return scalar_result.unique().all()

    async def get_item(self, product_id: int) -> Optional[ProductOrm]:
        """Get product by ID."""
        return await self._get(product_id)

    async def create(self, creation_data: ProductRequest) -> ProductOrm:
        """Saves the model record to the database."""
        async with self._session.begin():
            operation = ProductOrm(**creation_data.dict())
            self._session.add(operation)
            await self._session.commit()

        await self._session.refresh(operation)
        return operation

    async def update(self, product_id: int, request: ProductRequest) -> Optional[ProductOrm]:
        """Updating product."""
        operation = await self._get(product_id)
        if operation:
            for field, value in request.dict().items():
                setattr(operation, field, value)
            await self._session.commit()
            await self._session.refresh(operation)
        return operation

    async def delete(self, product_id: int) -> Optional[ProductOrm]:
        """Deleted product."""
        operation = await self._get(product_id)
        if operation:
            await self._session.delete(operation)
            await self._session.commit()
            return operation

    async def _get(self, product_id: int) -> Optional[ProductOrm]:
        """Get product by id."""
        try:
            async with self._session.begin():
                result = await self._session.execute(
                    select(ProductOrm).where(ProductOrm.id == product_id),
                )
                return result.scalar_one_or_none()
        except (OSError, SQLAlchemyError) as error_msg:
            ...
            # logging.info(f'Error with Database: {error_msg}')
