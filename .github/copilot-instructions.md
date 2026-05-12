---
name: TechShop Project Guidelines
description: "Enforce TechShop coding standards: Python type annotations, Google-style docstrings, PEP 8, Black formatting, AAA test pattern, FastAPI/Pydantic stack, security and performance focus"
applyTo: "src/**/*.py"
---

# TechShop Project Instructions

You are assisting with **TechShop**, an e-commerce platform MVP focused on cart management, checkout, and product visualization with emphasis on **security**, **performance**, and **scalability**.

## Tech Stack & Architecture

- **Language:** Python 3.x
- **Web Framework:** FastAPI
- **Data Validation:** Pydantic
- **Database:** PostgreSQL (planned)
- **Code Formatter:** Black
- **Code Style:** PEP 8
- **Type Checker:** mypy

## Mandatory Code Standards

### 1. Type Annotations (mypy-compatible)

**All functions, methods, and class attributes MUST have type hints.** This is non-negotiable.

```python
# ✅ CORRECT
def add_to_cart(user_id: int, product_id: int, quantity: int) -> dict[str, Any]:
    """Add an item to the user's cart."""
    ...

class Product:
    id: int
    name: str
    price: float

# ❌ WRONG - No type hints
def add_to_cart(user_id, product_id, quantity):
    ...
```

### 2. Docstrings (Google Style Guide)

**Every function, method, and class MUST have a docstring.** Use Google Style Guide format:

```python
# ✅ CORRECT
def calculate_cart_total(cart_items: list[CartItem]) -> float:
    """Calculate the total price of all items in the cart.
    
    Args:
        cart_items: A list of CartItem objects in the shopping cart.
    
    Returns:
        The total price as a float, including all items.
        
    Raises:
        ValueError: If cart_items is empty.
    """
    if not cart_items:
        raise ValueError("Cart cannot be empty")
    return sum(item.price * item.quantity for item in cart_items)

# ❌ WRONG - Missing docstring or unclear format
def calculate_cart_total(cart_items: list[CartItem]) -> float:
    return sum(item.price * item.quantity for item in cart_items)
```

### 3. Unit Tests (AAA Pattern)

**All unit tests MUST follow the Arrange, Act, Assert (AAA) pattern.** Structure:
- **Arrange:** Set up test data and conditions
- **Act:** Execute the function being tested
- **Assert:** Verify the results

```python
# ✅ CORRECT - AAA Pattern
def test_add_to_cart_success():
    # Arrange
    user_id = 1
    product = Product(id=1, name="Laptop", price=999.99)
    cart = Cart(user_id=user_id)
    
    # Act
    cart.add_item(product, quantity=1)
    
    # Assert
    assert len(cart.items) == 1
    assert cart.items[0].product_id == 1

# ❌ WRONG - Unclear structure, mixed concerns
def test_add_to_cart_success():
    user_id = 1
    product = Product(id=1, name="Laptop", price=999.99)
    cart = Cart(user_id=user_id)
    cart.add_item(product, quantity=1)
    assert len(cart.items) == 1
```

### 4. Code Style

- **Follow PEP 8** strictly
- **Use Black formatter** for all Python files
- **Max line length:** 88 characters (Black default)
- **Imports:** Organize as standard library → third-party → local imports

```python
# ✅ CORRECT - Proper organization and formatting
import json
from typing import Any, Optional

import fastapi
from pydantic import BaseModel

from src.models import Product, Cart
```

## Domain-Specific Guidelines

### Cart Management
- All cart operations must validate user ownership
- Calculate totals consistently (use a dedicated function)
- Implement quantity constraints (min 1, max reasonable limit)

### Checkout & Security
- All sensitive data must be encrypted
- Never log passwords or payment information
- Validate all user inputs with Pydantic models

### Performance & Scalability
- Use database indexes on frequently queried fields (`user_id`, `product_id`)
- Implement pagination for product listings
- Cache cart data appropriately

## File Structure & Models

Follow the provided Entity-Relationship model:
- **Product:** `id`, `name`, `price`
- **Cart:** `id`, `user_id`
- **CartItem:** Links products to carts with `quantity`

Use Pydantic for all data models and validation.

## When to Ask for Clarification

Ask the user before:
- Implementing database operations (schema may not be finalized)
- Adding new features outside cart/checkout (scope unclear)
- Choosing between alternative approaches for non-obvious design decisions

## Common Reminders

✅ **Do:**
- Include type hints on every function and class
- Write clear, focused docstrings
- Test with AAA pattern
- Format with Black
- Validate inputs with Pydantic
- Consider security implications

❌ **Don't:**
- Skip docstrings or type annotations
- Mix multiple concerns in a single function
- Write tests without clear arrange/act/assert structure
- Log sensitive information
- Ignore performance implications of database queries
