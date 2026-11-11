"""Наследники Product: Smartphone, LawnGrass, сложение и защита add_product."""

from typing import Any

import pytest

from src.category import Category, CategoryIterator
from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone


@pytest.fixture(autouse=True)
def reset_counts(monkeypatch: pytest.MonkeyPatch) -> None:
    """Изолирует счётчики категорий и восстанавливает их после теста."""
    monkeypatch.setattr(Category, "category_count", 0)
    monkeypatch.setattr(Category, "product_count", 0)


@pytest.fixture
def smartphone() -> Smartphone:
    return Smartphone(
        "Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space"
    )


@pytest.fixture
def smartphone2() -> Smartphone:
    return Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )


@pytest.fixture
def grass() -> LawnGrass:
    return LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )


@pytest.fixture
def grass2() -> LawnGrass:
    return LawnGrass(
        "Газонная трава 2",
        "Выносливая трава",
        450.0,
        15,
        "США",
        "5 дней",
        "Темно-зеленый",
    )


def test_smartphone_attributes(smartphone: Smartphone) -> None:
    assert smartphone.name == "Iphone 15"
    assert smartphone.description == "512GB, Gray space"
    assert smartphone.price == 210000.0
    assert smartphone.quantity == 8
    assert smartphone.efficiency == 98.2
    assert smartphone.model == "15"
    assert smartphone.memory == 512
    assert smartphone.color == "Gray space"


def test_lawn_grass_attributes(grass: LawnGrass) -> None:
    assert grass.name == "Газонная трава"
    assert grass.description == "Элитная трава для газона"
    assert grass.price == 500.0
    assert grass.quantity == 20
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"


def test_classes_inherit_product(smartphone: Smartphone, grass: LawnGrass) -> None:
    assert issubclass(Smartphone, Product)
    assert issubclass(LawnGrass, Product)
    assert isinstance(smartphone, Product)
    assert isinstance(grass, Product)
    assert not issubclass(Smartphone, LawnGrass)


def test_subclass_uses_product_str(smartphone: Smartphone) -> None:
    assert str(smartphone) == "Iphone 15, 210000.0 руб. Остаток: 8 шт."


def test_subclass_price_setter_is_inherited(
    smartphone: Smartphone, monkeypatch: pytest.MonkeyPatch
) -> None:
    smartphone.price = 250000.0
    assert smartphone.price == 250000.0
    monkeypatch.setattr("builtins.input", lambda prompt: "y")
    smartphone.price = 100.0
    assert smartphone.price == 100.0
    smartphone.price = -5
    assert smartphone.price == 100.0


def test_add_same_class(
    smartphone: Smartphone,
    smartphone2: Smartphone,
    grass: LawnGrass,
    grass2: LawnGrass,
) -> None:
    assert smartphone + smartphone2 == 2580000.0
    assert grass + grass2 == 16750.0


def test_add_plain_products_still_works() -> None:
    assert Product("a", "d", 100, 10) + Product("b", "d", 200, 2) == 1400


def test_add_different_classes_raises(smartphone: Smartphone, grass: LawnGrass) -> None:
    with pytest.raises(TypeError):
        smartphone + grass
    with pytest.raises(TypeError):
        grass + smartphone


def test_add_base_and_subclass_raises(smartphone: Smartphone) -> None:
    base = Product("a", "d", 100, 10)
    with pytest.raises(TypeError):
        base + smartphone
    with pytest.raises(TypeError):
        smartphone + base


def test_add_requires_exact_type(smartphone: Smartphone) -> None:
    class ProSmartphone(Smartphone):
        pass

    pro = ProSmartphone("Pro", "d", 1.0, 1, 1.0, "m", 1, "c")
    with pytest.raises(TypeError):
        smartphone + pro


def test_failed_add_keeps_operands(smartphone: Smartphone, grass: LawnGrass) -> None:
    with pytest.raises(TypeError):
        smartphone + grass
    assert (smartphone.price, smartphone.quantity) == (210000.0, 8)
    assert (grass.price, grass.quantity) == (500.0, 20)


def test_add_product_accepts_product_and_subclasses(
    smartphone: Smartphone, grass: LawnGrass
) -> None:
    category = Category("Разное", "", [])
    category.add_product(smartphone)
    category.add_product(grass)
    category.add_product(Product("Кабель", "", 80, 15))
    assert category.product_list[:2] == [smartphone, grass]
    assert Category.product_count == 3
    assert str(category) == "Разное, количество продуктов: 43 шт."


@pytest.mark.parametrize(
    "bad",
    [
        "Not a product",
        1,
        2.5,
        None,
        {"name": "x"},
        [Product("a", "", 1, 1)],
        Product,
        object(),
    ],
)
def test_add_product_rejects_other_objects(bad: Any) -> None:
    category = Category("Пустая", "", [])
    with pytest.raises(TypeError):
        category.add_product(bad)
    assert category.products == ""
    assert Category.product_count == 0


def test_mixed_category_iteration(smartphone: Smartphone, grass: LawnGrass) -> None:
    category = Category("Смесь", "", [smartphone, grass])
    assert [type(item) for item in CategoryIterator(category)] == [
        Smartphone,
        LawnGrass,
    ]
    assert category.products == (
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
        "Газонная трава, 500.0 руб. Остаток: 20 шт.\n"
    )
