from unittest.mock import patch

import pytest

from src.products import Category, LawnGrass, Product, Smartphone


# Фикстуры
@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 100.0, 10)


@pytest.fixture
def sample_smartphone():
    return Smartphone("Smartphone", "Desc", 50000.0, 5, 95.5, "Model X", 256, "Black")


@pytest.fixture
def sample_lawn_grass():
    return LawnGrass("Grass", "Desc", 500.0, 20, "Russia", "14 дней", "Green")


@pytest.fixture
def sample_category(sample_product):
    return Category("Test Category", "Test Category Description", [sample_product])


def test_product_price_setter_positive(sample_product):
    sample_product.price = 150.0
    assert sample_product.price == 150.0


def test_product_price_setter_negative(capsys, sample_product):
    sample_product.price = -50.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 100.0


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
    assert product.quantity == 15
    assert product.price == 60.0


# Тесты для новых классов (Smartphone и LawnGrass)
def test_smartphone_creation(sample_smartphone):
    assert sample_smartphone.memory == 256
    assert isinstance(sample_smartphone, Product)


def test_lawn_grass_creation(sample_lawn_grass):
    assert sample_lawn_grass.country == "Russia"
    assert isinstance(sample_lawn_grass, Product)


def test_add_smartphones(sample_smartphone):
    smartphone2 = Smartphone("Smart2", "Desc", 60000.0, 3, 98.0, "Model Y", 512, "White")
    total = sample_smartphone + smartphone2
    assert total == 50000.0 * 5 + 60000.0 * 3


def test_add_different_types(sample_smartphone, sample_lawn_grass):
    with pytest.raises(TypeError):
        sample_smartphone + sample_lawn_grass


# Тесты для Category (старые + новые)
def test_empty_category():
    category = Category("Empty", "Desc", [])
    assert str(category) == "Empty, количество продуктов: 0 шт."
    assert category.products == ""


def test_category_add_product(sample_category):
    new_product = Product("New", "Desc", 200.0, 3)
    sample_category.add_product(new_product)
    assert "New, 200.0 руб. Остаток: 3 шт." in sample_category.products


def test_category_add_invalid_product(sample_category):
    with pytest.raises(TypeError):
        sample_category.add_product("Not a product")


def test_category_add_smartphone(sample_category, sample_smartphone):
    sample_category.add_product(sample_smartphone)
    assert "Smartphone, 50000.0 руб. Остаток: 5 шт." in sample_category.products


# Тесты для CategoryIterator
def test_iterator_empty_category():
    category = Category("Empty", "Desc", [])
    products = list(category)
    assert len(products) == 0


def test_iterator_with_products(sample_category):
    products = list(sample_category)
    assert len(products) == 1
    assert products[0].name == "Test Product"
