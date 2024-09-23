from sqlalchemy import Column, Integer, String, DateTime

from app.storages.models.base_model import Base


class Order(Base):
    __tablename__ = 'orders'

    created_at = Column(DateTime)
    status = Column(String)


