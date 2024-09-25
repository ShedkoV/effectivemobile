from abc import ABC
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.storages.models.base_model import BaseOrm


class BaseService(ABC):
    """Базовый класс для реализации CRUD-операций у классов наследников."""

    def __init__(self, session: AsyncSession, model: BaseOrm) -> None:
        self._session = session
        self._model = model

    async def get_obj_or_none(self, obj_id: int) -> Optional[BaseOrm]:
        """Возвращает объект модели из БД по `id` или `None` при отсутствии."""
        try:
            return await self._session.get(self._model, obj_id)
        except (OSError, SQLAlchemyError) as error_msg:
            print(error_msg)

    async def get_item(self, obj_id: int) -> Optional[BaseOrm]:
        """Возвращает объект модели из БД по `id` или ошибку `404`."""
        target_obj = await self.get_obj_or_none(obj_id)
        if not target_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return target_obj

    async def get_all_items(self) -> list[BaseOrm]:
        """Возвращает список всех объектов модели."""
        scalar_result = await self._session.scalars(
            select(self._model).order_by(self._model.id),
        )

        return scalar_result.unique().all()  # type: ignore[return-value]

    async def create(self, request: BaseModel) -> BaseOrm:
        """Saves the model record to the database."""
        async with self._session.begin():
            operation = self._model(**request.dict())
            self._session.add(operation)
            await self._session.commit()
        await self._session.refresh(operation)

        return operation

    async def update(self, obj_id: int, request: BaseModel) -> Optional[BaseOrm]:
        """Updating product."""
        operation = await self.get_item(obj_id)
        if operation:
            for field, value in request.dict().items():
                setattr(operation, field, value)
            await self._session.commit()
            await self._session.refresh(operation)

        return operation

    async def delete(self, obj_id: int) -> Optional[BaseOrm]:
        """Deleted product."""
        operation = await self.get_item(obj_id)
        await self._session.delete(operation)
        await self._session.commit()

        return operation
