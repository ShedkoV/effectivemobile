from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base_service import BaseService
from app.storages.database import get_session
from app.storages.models import ProductOrm


class ProductService(BaseService):
    """Класс, для операций на эндпоинтах /orders"""
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> None:
        super().__init__(session, ProductOrm)
