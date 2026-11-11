"""Трава газонная — наследник Product со сведениями о производителе."""

from src.product import Product


class LawnGrass(Product):
    """Товар «Трава газонная»: страна, срок прорастания и цвет."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
