from unittest.mock import patch

import pytest

from src.products import Category, Product


# Фикстуры
@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 100.0, 10)


@pytest.fixture
def sample_category(sample_product):
    return Category("Test Category", "Test Category Description", [sample_product])


# Тесты для Product
def test_product_price_setter_positive(sample_product):
    sample_product.price = 150.0
    assert sample_product.price == 150.0


def test_product_price_setter_negative(capsys, sample_product):
    sample_product.price = -50.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 100.0  # Цена не изменилась


@patch("builtins.input", return_value="y")
def test_price_decrease_confirmation(mock_input, sample_product):
    sample_product.price = 80.0
    assert sample_product.price == 80.0


def test_product_addition_type_error(sample_product):
    with pytest.raises(TypeError):
        sample_product + "not a product"


def test_new_product_with_duplicate():
    existing = Product("Duplicate", "Desc", 50.0, 10)
    new_data = {"name": "Duplicate", "description": "New Desc", "price": 60.0, "quantity": 5}
    product = Product.new_product(new_data, [existing])
    assert product.quantity == 15  # 10 + 5
    assert product.price == 60.0  # Выбрана более высокая цена


# Тесты для Category
def test_empty_category():
    category = Category("Empty", "Desc", [])
    assert str(category) == "Empty, количество продуктов: 0 шт."
    assert category.products == ""


def test_category_add_product(sample_category):
    new_product = Product("New", "Desc", 200.0, 3)
    sample_category.add_product(new_product)
    assert "New, 200.0 руб. Остаток: 3 шт." in sample_category.products


# Тесты для CategoryIterator
def test_iterator_empty_category():
    category = Category("Empty", "Desc", [])
    products = list(category)  # Преобразуем итератор в список
    assert len(products) == 0


def test_iterator_with_products(sample_category):
    products = list(sample_category)
    assert len(products) == 1
    assert products[0].name == "Test Product"
