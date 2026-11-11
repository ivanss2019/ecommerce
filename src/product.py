"""Товар интернет-магазина с защищённой ценой."""

from typing import Any, Dict, List, Optional, Type, TypeVar

ProductType = TypeVar("ProductType", bound="Product")


class Product:
    """Хранит свойства товара и контролирует изменение цены."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Возвращает текущую цену."""
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """Отклоняет неположительную цену, снижение требует ответа y."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if value < self.__price:
            answer = input("Подтвердить снижение цены? (y/n): ")
            if answer != "y":
                return
        self.__price = value

    def __str__(self) -> str:
        """Строка вида «Название, 80 руб. Остаток: 15 шт.»."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: object) -> float:
        """Возвращает суммарную стоимость остатков двух товаров на складе.

        Для не-Product возвращает NotImplemented, и Python сам поднимает
        TypeError вместо молчаливого неверного результата.
        """
        if not isinstance(other, Product):
            return NotImplemented
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(
        cls: Type[ProductType],
        data: Dict[str, Any],
        products: Optional[List["Product"]] = None,
    ) -> ProductType:
        """Создаёт товар из словаря, объединяя совпадения имени в новом объекте.

        Имя сравнивается без регистра и крайних пробелов. Количества всех
        совпадений складываются, выбирается максимальная цена. Переданный
        список и его объекты не изменяются; описание берётся из словаря.
        """
        quantity = data["quantity"]
        price = data["price"]
        for product in products or []:
            if product.name.strip().casefold() == data["name"].strip().casefold():
                quantity += product.quantity
                price = max(price, product.price)
        return cls(data["name"], data["description"], price, quantity)
