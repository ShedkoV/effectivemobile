from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, as_declarative, declared_attr, mapped_column


@as_declarative()
class BaseOrm:
    """Базовая модель."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
