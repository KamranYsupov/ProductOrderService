from app.db import Product
from .base import RepositoryBase


class RepositoryProduct(RepositoryBase[Product]):
    """Репозиторий для работы с таблицей products"""