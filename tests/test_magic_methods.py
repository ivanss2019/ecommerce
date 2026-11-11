"""Магические методы: __str__, __add__ и итерация по товарам категории."""

from typing import List

import pytest

from src.category import Category, CategoryIterator
from src.product import Product


@pytest.fixture
def product_a() -> Product:
    return Product("Название продукта", "Описание", 80, 15)


@pytest.fixture
def products() -> List[Product]:
    return [Product("A", "d", 100, 10), Product("B", "d", 200, 2)]


@pytest.fixture
def category(products: List[Product]) -> Category:
    return Category("Смартфоны", "Описание", products)


def test_product_str(product_a: Product) -> None:
    assert str(product_a) == "Название продукта, 80 руб. Остаток: 15 шт."


def test_product_str_float_price() -> None:
    product = Product("Телефон", "", 12345.5, 100)
    assert str(product) == "Телефон, 12345.5 руб. Остаток: 100 шт."


def test_product_str_follows_changes(product_a: Product) -> None:
    product_a.quantity = 3
    product_a.price = 90
    assert str(product_a) == "Название продукта, 90 руб. Остаток: 3 шт."


def test_product_add(products: List[Product]) -> None:
    assert products[0] + products[1] == 1400


def test_product_add_is_commutative(products: List[Product]) -> None:
    assert products[0] + products[1] == products[1] + products[0]


def test_product_add_with_zero_quantity() -> None:
    assert Product("a", "", 100, 0) + Product("b", "", 200, 2) == 400


def test_product_add_does_not_change_operands(products: List[Product]) -> None:
    products[0] + products[1]
    assert (products[0].quantity, products[0].price) == (10, 100)
    assert (products[1].quantity, products[1].price) == (2, 200)


@pytest.mark.parametrize("other", [5, "строка", None, 1.5])
def test_product_add_wrong_type(product_a: Product, other: object) -> None:
    with pytest.raises(TypeError):
        product_a + other  # type: ignore[operator]
    with pytest.raises(TypeError):
        other + product_a  # type: ignore[operator]


def test_category_str(category: Category) -> None:
    assert str(category) == "Смартфоны, количество продуктов: 12 шт."


def test_category_str_empty() -> None:
    assert str(Category("Пустая", "", [])) == "Пустая, количество продуктов: 0 шт."


def test_category_str_after_add_product(category: Category) -> None:
    category.add_product(Product("C", "d", 1, 8))
    assert str(category) == "Смартфоны, количество продуктов: 20 шт."


def test_products_getter_uses_product_str(category: Category) -> None:
    assert (
        category.products == "A, 100 руб. Остаток: 10 шт.\nB, 200 руб. Остаток: 2 шт.\n"
    )


def test_product_list_is_a_copy(category: Category) -> None:
    items = category.product_list
    items.clear()
    assert len(category.product_list) == 2


def test_category_iterator(category: Category, products: List[Product]) -> None:
    assert list(CategoryIterator(category)) == products


def test_category_iterator_for_loop(category: Category) -> None:
    names = [product.name for product in CategoryIterator(category)]
    assert names == ["A", "B"]


def test_category_iterator_next_and_stop(category: Category) -> None:
    iterator = CategoryIterator(category)
    assert next(iterator).name == "A"
    assert next(iterator).name == "B"
    with pytest.raises(StopIteration):
        next(iterator)


def test_category_iterator_restarts(category: Category) -> None:
    iterator = CategoryIterator(category)
    assert len(list(iterator)) == 2
    assert len(list(iterator)) == 2


def test_category_iterator_empty() -> None:
    assert list(CategoryIterator(Category("Пустая", "", []))) == []


def test_iterator_sees_added_product_on_new_iteration(category: Category) -> None:
    iterator = CategoryIterator(category)
    category.add_product(Product("C", "d", 1, 1))
    assert [product.name for product in iterator] == ["A", "B", "C"]
