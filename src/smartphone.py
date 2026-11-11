"""Смартфон — наследник Product с техническими характеристиками."""

from src.product import Product


class Smartphone(Product):
    """Товар «Смартфон»: производительность, модель, память и цвет."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
