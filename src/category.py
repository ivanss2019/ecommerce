"""Категории товаров с приватным списком и общими счётчиками."""

from typing import ClassVar, List

from src.product import Product


class Category:
    """Добавляет товары через метод, предоставляет строку для просмотра."""

    category_count: ClassVar[int] = 0
    product_count: ClassVar[int] = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = list(products)
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет объект Product и обновляет общее количество позиций."""
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавить только объект Product")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает по одной строке на товар; пустая категория — пустая строка."""
        return "".join(f"{product}\n" for product in self.__products)

    @property
    def product_list(self) -> List[Product]:
        """Возвращает копию списка товаров; изменение копии категорию не меняет."""
        return list(self.__products)

    def __str__(self) -> str:
        """Строка вида «Название, количество продуктов: 200 шт.» (сумма остатков)."""
        total = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total} шт."

