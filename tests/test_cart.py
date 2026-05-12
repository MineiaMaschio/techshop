"""Unit tests for ShoppingCart class using pytest with AAA pattern.

This module contains comprehensive tests for the ShoppingCart class,
covering happy paths (successful operations) and edge cases.
All tests follow the Arrange, Act, Assert (AAA) pattern.
"""

from typing import List

import pytest

from src.cart import ShoppingCart
from src.models import CartItem, Product


# Fixtures para dados reutilizáveis
@pytest.fixture
def product_laptop() -> Product:
    """Create a sample laptop product for testing."""
    return Product(id=1, name="Laptop", price=999.99)


@pytest.fixture
def product_mouse() -> Product:
    """Create a sample mouse product for testing."""
    return Product(id=2, name="Mouse", price=50.00)


@pytest.fixture
def product_keyboard() -> Product:
    """Create a sample keyboard product for testing."""
    return Product(id=3, name="Keyboard", price=150.00)


@pytest.fixture
def empty_cart() -> ShoppingCart:
    """Create an empty shopping cart for testing."""
    return ShoppingCart()


# ============================================================================
# HAPPY PATH TESTS - Successful operations
# ============================================================================


class TestAddItemHappyPath:
    """Tests for successful item addition scenarios."""

    def test_add_single_item_to_empty_cart(
        self, empty_cart: ShoppingCart, product_laptop: Product
    ) -> None:
        """Test adding a single item to an empty cart.

        Verifies that an item is correctly added to the cart and
        the cart contains exactly one item.
        """
        # Arrange
        cart = empty_cart
        quantity = 1

        # Act
        cart.add_item(product_laptop, quantity)

        # Assert
        assert len(cart.items) == 1
        assert cart.items[0].product.id == product_laptop.id
        assert cart.items[0].quantity == 1

    def test_add_multiple_different_items(
        self,
        empty_cart: ShoppingCart,
        product_laptop: Product,
        product_mouse: Product,
    ) -> None:
        """Test adding multiple different items to the cart.

        Verifies that multiple items can be added without duplication
        and each maintains its own quantity.
        """
        # Arrange
        cart = empty_cart

        # Act
        cart.add_item(product_laptop, 1)
        cart.add_item(product_mouse, 2)

        # Assert
        assert len(cart.items) == 2
        assert cart.items[0].product.id == product_laptop.id
        assert cart.items[0].quantity == 1
        assert cart.items[1].product.id == product_mouse.id
        assert cart.items[1].quantity == 2

    def test_add_same_product_multiple_times(
        self, empty_cart: ShoppingCart, product_laptop: Product
    ) -> None:
        """Test adding the same product multiple times increases quantity.

        Verifies that when adding a product that already exists,
        the quantity is incremented rather than creating a duplicate.
        """
        # Arrange
        cart = empty_cart

        # Act
        cart.add_item(product_laptop, 1)
        cart.add_item(product_laptop, 2)

        # Assert
        assert len(cart.items) == 1
        assert cart.items[0].quantity == 3

    def test_add_item_with_large_quantity(
        self, empty_cart: ShoppingCart, product_mouse: Product
    ) -> None:
        """Test adding an item with a large quantity.

        Verifies that quantities greater than 1 are handled correctly
        when adding a new item.
        """
        # Arrange
        cart = empty_cart
        quantity = 100

        # Act
        cart.add_item(product_mouse, quantity)

        # Assert
        assert len(cart.items) == 1
        assert cart.items[0].quantity == 100


class TestRemoveItemHappyPath:
    """Tests for successful item removal scenarios."""

    def test_remove_item_from_cart(
        self, empty_cart: ShoppingCart, product_laptop: Product
    ) -> None:
        """Test removing an item from the cart.

        Verifies that the correct item is removed and the cart
        reflects the change.
        """
        # Arrange
        cart = empty_cart
        cart.add_item(product_laptop, 1)

        # Act
        cart.remove_item(product_laptop.id)

        # Assert
        assert len(cart.items) == 0

    def test_remove_specific_item_from_multiple_items(
        self,
        empty_cart: ShoppingCart,
        product_laptop: Product,
        product_mouse: Product,
        product_keyboard: Product,
    ) -> None:
        """Test removing one item while keeping others.

        Verifies that removing an item affects only the target item
        and leaves other items untouched.
        """
        # Arrange
        cart = empty_cart
        cart.add_item(product_laptop, 1)
        cart.add_item(product_mouse, 2)
        cart.add_item(product_keyboard, 1)

        # Act
        cart.remove_item(product_mouse.id)

        # Assert
        assert len(cart.items) == 2
        assert all(item.product.id != product_mouse.id for item in cart.items)
        assert any(item.product.id == product_laptop.id for item in cart.items)
        assert any(item.product.id == product_keyboard.id for item in cart.items)


class TestCalculateTotalHappyPath:
    """Tests for successful total calculation scenarios."""

    def test_calculate_total_single_item(
        self, empty_cart: ShoppingCart, product_laptop: Product
    ) -> None:
        """Test calculating total for a single item.

        Verifies that the total is correctly calculated as
        price * quantity.
        """
        # Arrange
        cart = empty_cart
        cart.add_item(product_laptop, 1)

        # Act
        total = cart.calculate_total()

        # Assert
        assert total == pytest.approx(999.99)

    def test_calculate_total_multiple_items(
        self,
        empty_cart: ShoppingCart,
        product_laptop: Product,
        product_mouse: Product,
    ) -> None:
        """Test calculating total for multiple items.

        Verifies that the total correctly sums up the cost of
        all items in the cart.
        """
        # Arrange
        cart = empty_cart
        cart.add_item(product_laptop, 1)  # 999.99
        cart.add_item(product_mouse, 2)  # 50.00 * 2 = 100.00

        # Act
        total = cart.calculate_total()

        # Assert
        assert total == pytest.approx(1099.99)

    def test_calculate_total_with_same_product_multiple_quantities(
        self, empty_cart: ShoppingCart, product_mouse: Product
    ) -> None:
        """Test calculating total when same product added multiple times.

        Verifies that the total accounts for combined quantities
        of the same product.
        """
        # Arrange
        cart = empty_cart
        cart.add_item(product_mouse, 5)
        cart.add_item(product_mouse, 3)

        # Act
        total = cart.calculate_total()

        # Assert
        assert total == pytest.approx(400.00)  # 50.00 * 8


class TestDiscountCalculationHappyPath:
    """Tests for successful discount calculation scenarios."""

    def test_calculate_total_no_discount_below_500(
        self, empty_cart: ShoppingCart, product_mouse: Product
    ) -> None:
        """Test that no discount is applied for purchases below R$ 500.

        Verifies that when total is below 500, the discount is 0%.
        """
        # Arrange
        cart = empty_cart
        cart.add_item(product_mouse, 5)  # 50.00 * 5 = 250.00

        # Act
        total_with_discount = cart.calculate_total_with_discount()

        # Assert
        assert total_with_discount == pytest.approx(250.00)

    def test_calculate_total_with_10_percent_discount(
        self, empty_cart: ShoppingCart, product_keyboard: Product
    ) -> None:
        """Test that 10% discount is applied for purchases above R$ 500.

        Verifies that when total is between 500 and 1000,
        a 10% discount is applied.
        """
        # Arrange
        cart = empty_cart
        cart.add_item(product_keyboard, 4)  # 150.00 * 4 = 600.00

        # Act
        total_with_discount = cart.calculate_total_with_discount()

        # Assert
        expected = 600.00 * 0.90
        assert total_with_discount == pytest.approx(expected)

    def test_calculate_total_with_20_percent_discount(
        self, empty_cart: ShoppingCart, product_laptop: Product
    ) -> None:
        """Test that 20% discount is applied for purchases above R$ 1000.

        Verifies that when total exceeds 1000,
        a 20% discount is applied.
        """
        # Arrange
        cart = empty_cart
        cart.add_item(product_laptop, 2)  # 999.99 * 2 = 1999.98

        # Act
        total_with_discount = cart.calculate_total_with_discount()

        # Assert
        expected = 1999.98 * 0.80
        assert total_with_discount == pytest.approx(expected)


# ============================================================================
# EDGE CASE TESTS - Boundary conditions and unusual scenarios
# ============================================================================


class TestEmptyCartEdgeCases:
    """Tests for empty cart edge cases."""

    def test_calculate_total_empty_cart(self, empty_cart: ShoppingCart) -> None:
        """Test calculating total for an empty cart.

        Verifies that the total of an empty cart is 0.
        """
        # Arrange
        cart = empty_cart

        # Act
        total = cart.calculate_total()

        # Assert
        assert total == 0.0

    def test_calculate_total_with_discount_empty_cart(
        self, empty_cart: ShoppingCart
    ) -> None:
        """Test calculating discounted total for an empty cart.

        Verifies that the discounted total of an empty cart is 0.
        """
        # Arrange
        cart = empty_cart

        # Act
        total_with_discount = cart.calculate_total_with_discount()

        # Assert
        assert total_with_discount == 0.0

    def test_remove_item_from_empty_cart(self, empty_cart: ShoppingCart) -> None:
        """Test removing an item from an empty cart.

        Verifies that removing from an empty cart does not raise
        an error and cart remains empty.
        """
        # Arrange
        cart = empty_cart

        # Act
        cart.remove_item(999)

        # Assert
        assert len(cart.items) == 0


class TestDiscountBoundaryEdgeCases:
    """Tests for discount threshold boundary conditions."""

    def test_discount_exactly_at_500_threshold(
        self, empty_cart: ShoppingCart
    ) -> None:
        """Test discount behavior exactly at R$ 500 threshold.

        Verifies that a total of exactly R$ 500 does NOT qualify
        for the 10% discount (threshold is > 500, not >= 500).
        """
        # Arrange
        cart = empty_cart
        product_500 = Product(id=10, name="Product500", price=500.00)

        # Act
        cart.add_item(product_500, 1)
        total_with_discount = cart.calculate_total_with_discount()

        # Assert
        assert total_with_discount == pytest.approx(500.00)

    def test_discount_just_above_500_threshold(
        self, empty_cart: ShoppingCart
    ) -> None:
        """Test discount behavior just above R$ 500 threshold.

        Verifies that a total just above R$ 500 qualifies
        for the 10% discount.
        """
        # Arrange
        cart = empty_cart
        product_501 = Product(id=11, name="Product501", price=500.10)

        # Act
        cart.add_item(product_501, 1)
        total_with_discount = cart.calculate_total_with_discount()

        # Assert
        expected = 500.10 * 0.90
        assert total_with_discount == pytest.approx(expected)

    def test_discount_exactly_at_1000_threshold(
        self, empty_cart: ShoppingCart
    ) -> None:
        """Test discount behavior exactly at R$ 1000 threshold.

        Verifies that a total of exactly R$ 1000 does NOT qualify
        for the 20% discount (threshold is > 1000, not >= 1000).
        """
        # Arrange
        cart = empty_cart
        product_1000 = Product(id=12, name="Product1000", price=1000.00)

        # Act
        cart.add_item(product_1000, 1)
        total_with_discount = cart.calculate_total_with_discount()

        # Assert
        expected = 1000.00 * 0.90  # Should get 10% discount, not 20%
        assert total_with_discount == pytest.approx(expected)

    def test_discount_just_above_1000_threshold(
        self, empty_cart: ShoppingCart
    ) -> None:
        """Test discount behavior just above R$ 1000 threshold.

        Verifies that a total just above R$ 1000 qualifies
        for the 20% discount.
        """
        # Arrange
        cart = empty_cart
        product_1001 = Product(id=13, name="Product1001", price=1000.10)

        # Act
        cart.add_item(product_1001, 1)
        total_with_discount = cart.calculate_total_with_discount()

        # Assert
        expected = 1000.10 * 0.80  # Should get 20% discount
        assert total_with_discount == pytest.approx(expected)


class TestRemovalEdgeCases:
    """Tests for item removal edge cases."""

    def test_remove_nonexistent_item(
        self, empty_cart: ShoppingCart, product_laptop: Product
    ) -> None:
        """Test removing a product that doesn't exist in the cart.

        Verifies that removing a nonexistent item does not raise
        an error and cart remains unchanged.
        """
        # Arrange
        cart = empty_cart
        cart.add_item(product_laptop, 1)
        nonexistent_id = 999

        # Act
        cart.remove_item(nonexistent_id)

        # Assert
        assert len(cart.items) == 1
        assert cart.items[0].product.id == product_laptop.id

    def test_remove_all_items_sequentially(
        self,
        empty_cart: ShoppingCart,
        product_laptop: Product,
        product_mouse: Product,
    ) -> None:
        """Test removing all items from cart one by one.

        Verifies that items can be removed sequentially until
        the cart is empty.
        """
        # Arrange
        cart = empty_cart
        cart.add_item(product_laptop, 1)
        cart.add_item(product_mouse, 1)

        # Act
        cart.remove_item(product_laptop.id)
        cart.remove_item(product_mouse.id)

        # Assert
        assert len(cart.items) == 0


class TestQuantityEdgeCases:
    """Tests for quantity handling edge cases."""

    def test_add_item_with_zero_quantity(
        self, empty_cart: ShoppingCart, product_laptop: Product
    ) -> None:
        """Test adding an item with zero quantity.

        Verifies behavior when attempting to add an item with
        quantity of 0.
        """
        # Arrange
        cart = empty_cart

        # Act
        cart.add_item(product_laptop, 0)

        # Assert
        assert len(cart.items) == 1
        assert cart.items[0].quantity == 0

    def test_add_large_quantity_incrementally(
        self, empty_cart: ShoppingCart, product_mouse: Product
    ) -> None:
        """Test adding an item with incremental large quantities.

        Verifies that quantities accumulate correctly when adding
        the same item multiple times with large quantities.
        """
        # Arrange
        cart = empty_cart

        # Act
        for _ in range(10):
            cart.add_item(product_mouse, 10)

        # Assert
        assert len(cart.items) == 1
        assert cart.items[0].quantity == 100
