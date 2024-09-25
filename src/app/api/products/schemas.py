from pydantic import BaseModel, Field


class BaseProduct(BaseModel):
    """Базовый класс для запроса продукта в сервис и его ответа."""

    name: str = Field(
        ...,
        description='Название продукта',
    )
    description: str = Field(
        ...,
        description='Описание продукта',
    )
    price: float = Field(
        ...,
        description='Стоимость продукта',
    )
    quantity: int = Field(
        ...,
        description='Количество на складе',
    )


class ProductRequest(BaseProduct):
    """Запрос на создание продукта."""


class ProductResponse(BaseProduct):
    """Ответ принятого заказаю."""

    id: int = Field(
        ...,
        description='Уникальный номер',
    )

    class Config:
        """Orm mode on."""

        from_attributes = True
