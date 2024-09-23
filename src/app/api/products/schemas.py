from pydantic import BaseModel, Field


class BaseProduct(BaseModel):
    """..."""

    name: str = Field(
        description='Название продукта',
    )
    description: str = Field(
        description='Описание продукта',
    )
    price: float = Field(
        description='Стоимость продукта',
    )
    count: int = Field(
        description='Количество на складе',
    )


class ProductRequest(BaseProduct):
    """..."""


class ProductResponse(BaseProduct):
    id: int = Field(
        description='Уникальный номер',
    )

    class Config:
        """Orm mode on."""

        from_attributes = True
