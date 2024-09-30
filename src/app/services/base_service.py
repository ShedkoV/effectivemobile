from abc import ABC
from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.storages.models.base_model import BaseOrm


class BaseService(ABC):
    """Базовый класс для реализации CRUD-операций у классов наследников."""

    def __init__(self, session: AsyncSession, model: BaseOrm) -> None:
        self._session = session
        self._model = model
        self._relation_field = NotImplemented

    async def get_item(self, obj_id: int) -> Optional[BaseOrm]:
        """Возвращает объект модели из БД по `id` или ошибку `404`."""
        target_obj = await self._get_order_by_id(obj_id)
        if not target_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Запись с данным id({obj_id}) не найдена',
            )

        return target_obj

    async def get_all_items(self) -> list[BaseOrm]:
        """Получить все элементы необходимой таблицы."""
        result = await self._session.execute(
            select(self._model).options(selectinload(self._relation_field)),
        )
        return result.scalars().all()  # type: ignore[return-value]

    async def update(self, obj_id: int, request: BaseModel) -> Optional[BaseOrm]:
        """Обновить запись по её `id`."""
        operation = await self.get_item(obj_id)
        if operation:
            for field, value in request.dict().items():
                setattr(operation, field, value)
            await self._session.commit()
            await self._session.refresh(operation)

        return operation

    async def delete(self, obj_id: int) -> Optional[BaseOrm]:
        """Удалить запись по её `id`."""
        operation = await self.get_item(obj_id)
        await self._session.delete(operation)
        await self._session.commit()

        return operation

    async def _get_order_by_id(self, order_id: int) -> Optional[BaseOrm]:
        """Получить зпапись по её `id`."""
        result = await self._session.execute(
            select(self._model).options(selectinload(self._relation_field)).filter(self._model.id == order_id),  # noqa: E501, WPS221
        )
        return result.scalar_one_or_none()
