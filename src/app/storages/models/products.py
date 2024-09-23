from sqlalchemy import Column, Integer, String, Float

from app.storages.models.base_model import Base


class Product(Base):
    __tablename__ = 'products'

    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

