from dependency_injector import containers, providers

from app.repositories import (
    RepositoryProduct,
    RepositoryOrder,
    RepositoryOrderItem
)
from app.services import (
    ProductService,
    OrderService,
)
from app.db import (
    DataBaseManager,
    Product,
    Order,
    OrderItem,
)

from app.core.config import settings




class Container(containers.DeclarativeContainer):
    db_manager = providers.Singleton(DataBaseManager, db_url=settings.db_url)
    session = providers.Resource(db_manager().get_async_session)

    # region repository
    repository_product = providers.Singleton(
        RepositoryProduct, model=Product, session=session
    )
    repository_order = providers.Singleton(
        RepositoryOrder, model=Order, session=session
    )
    repository_order_item = providers.Singleton(
        RepositoryOrderItem, model=OrderItem, session=session
    )
    # endregion

    # region services
    product_service = providers.Singleton(
        ProductService,
        repository_product=repository_product,
    )
    order_service = providers.Singleton(
        OrderService,
        repository_product=repository_product,
        repository_order=repository_order,
        repository_order_item=repository_order_item,
    )
    # endregion


container = Container()
container.init_resources()
container.wire(modules=settings.container_wiring_modules)
