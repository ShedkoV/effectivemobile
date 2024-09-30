from datetime import datetime

import factory
from faker import Faker

from app.api.orders.schemas import OrderStatusEnum
from app.storages.models import OrderOrm, OrderItemOrm, ProductOrm


fake = Faker(locale='ru-RU')


class ProductOrmFactory(factory.Factory):
    id = factory.sequence(int)
    name = factory.sequence(str)
    description = factory.sequence(str)
    price = factory.sequence(float)
    quantity = factory.sequence(int)

    @factory.post_generation
    def order(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for order in extracted:
                self.order.append(order)

    @factory.post_generation
    def order_items(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for order_item in extracted:
                self.order_items.append(order_item)

    class Meta:
        model = ProductOrm


class OrderItemOrmFactory(factory.Factory):
    id = factory.sequence(int)
    product_id = factory.SubFactory(ProductOrmFactory)
    quantity = factory.sequence(int)

    class Meta:
        model = OrderItemOrm


class OrderOrmFactory(factory.Factory):

    created_at = datetime.utcnow()
    status = OrderStatusEnum.IN_PROCESS.value
    # product = factory.SubFactory(ProductOrmFactory)

    product_items = factory.RelatedFactoryList(OrderItemOrmFactory, factory_related_name='orders')

    class Meta:
        model = OrderOrm
