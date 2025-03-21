import unittest
from unittest import mock  # for simulating payment failures

# CartItem Class
class CartItem:
    """
    Represents an individual item in the shopping cart.
    
    Attributes:
        name (str): The item name.
        price (float): The item price.
        quantity (int): The quantity in the cart.
    """
    def __init__(self, name, price, quantity):
        """
        Initializes a CartItem.
        
        Args:
            name (str): Item name.
            price (float): Item price.
            quantity (int): Item quantity.
        """
        self.name = name
        self.price = price
        self.quantity = quantity

    def update_quantity(self, new_quantity):
        """
        Updates the quantity of the item.
        
        Args:
            new_quantity (int): The new quantity.
        """
        self.quantity = new_quantity

    def get_subtotal(self):
        """
        Calculates the subtotal price for this item.
        
        Returns:
            float: The subtotal price.
        """
        return self.price * self.quantity


# Cart Class
class Cart:
    """
    Represents a shopping cart containing CartItem objects.
    
    Attributes:
        items (list): List of CartItem objects.
    """
    def __init__(self):
        """Initializes an empty cart."""
        self.items = []

    def add_item(self, name, price, quantity):
        """
        Adds a new item to the cart or updates an existing one.
        
        Args:
            name (str): Item name.
            price (float): Item price.
            quantity (int): Quantity to add.
        
        Returns:
            str: Message indicating update or addition.
        """
        for item in self.items:
            if item.name == name:
                item.update_quantity(item.quantity + quantity)
                return f"Updated {name} quantity to {item.quantity}"
        new_item = CartItem(name, price, quantity)
        self.items.append(new_item)
        return f"Added {name} to cart"

    def remove_item(self, name):
        """
        Removes an item from the cart.
        
        Args:
            name (str): Name of the item to remove.
        
        Returns:
            str: Message indicating removal.
        """
        self.items = [item for item in self.items if item.name != name]
        return f"Removed {name} from cart"

    def update_item_quantity(self, name, new_quantity):
        """
        Updates the quantity of an item in the cart.
        
        Args:
            name (str): Item name.
            new_quantity (int): The new quantity.
        
        Returns:
            str: Message indicating update or not found.
        """
        for item in self.items:
            if item.name == name:
                item.update_quantity(new_quantity)
                return f"Updated {name} quantity to {new_quantity}"
        return f"{name} not found in cart"

    def calculate_total(self):
        """
        Calculates the total cost of the items in the cart, including tax and 
        delivery fee.
        
        Returns:
            dict: Contains 'subtotal', 'tax', 'delivery_fee', and 'total'.
        """
        subtotal = sum(item.get_subtotal() for item in self.items)
        tax = subtotal * 0.10  # Assume 10% tax rate.
        delivery_fee = 5.00    # Flat delivery fee.
        total = subtotal + tax + delivery_fee
        return {"subtotal": subtotal, "tax": tax,
                "delivery_fee": delivery_fee, "total": total}

    def view_cart(self):
        """
        Provides a view of the items in the cart.
        
        Returns:
            list: A list of dicts with item 'name', 'quantity', and 'subtotal'.
        """
        return [{"name": item.name, "quantity": item.quantity,
                 "subtotal": item.get_subtotal()} for item in self.items]


# OrderPlacement Class
class OrderPlacement:
    """
    Represents the process of placing an order.
    
    Attributes:
        cart (Cart): The shopping cart.
        user_profile (UserProfile): The user's profile.
        restaurant_menu (RestaurantMenu): The available menu items.
    """
    def __init__(self, cart, user_profile, restaurant_menu):
        """
        Initializes an OrderPlacement object.
        
        Args:
            cart (Cart): The shopping cart.
            user_profile (UserProfile): The user's profile.
            restaurant_menu (RestaurantMenu): The restaurant menu.
        """
        self.cart = cart
        self.user_profile = user_profile
        self.restaurant_menu = restaurant_menu

    def validate_order(self):
        """
        Validates the order by checking if the cart is empty and if all 
        items are available in the menu.
        
        Returns:
            dict: Contains 'success' and 'message'.
        """
        if not self.cart.items:
            return {"success": False, "message": "Cart is empty"}
        for item in self.cart.items:
            if not self.restaurant_menu.is_item_available(item.name):
                return {"success": False,
                        "message": f"{item.name} is not available"}
        return {"success": True, "message": "Order is valid"}

    def proceed_to_checkout(self):
        """
        Prepares the order for checkout by calculating totals and retrieving 
        the delivery address.
        
        Returns:
            dict: Contains 'items', 'total_info', and 'delivery_address'.
        """
        total_info = self.cart.calculate_total()
        return {"items": self.cart.view_cart(),
                "total_info": total_info,
                "delivery_address": self.user_profile.delivery_address}

    def confirm_order(self, payment_method):
        """
        Confirms the order by validating it and processing the payment.
        
        Args:
            payment_method (PaymentMethod): The payment method to use.
        
        Returns:
            dict: Contains 'success', 'message', and, if successful, an 
            order ID and estimated delivery time.
        """
        if not self.validate_order()["success"]:
            return {"success": False, "message": "Order validation failed"}
        total = self.cart.calculate_total()["total"]
        payment_success = payment_method.process_payment(total)
        if payment_success:
            return {"success": True, "message": "Order confirmed",
                    "order_id": "ORD123456", 
                    "estimated_delivery": "45 minutes"}
        return {"success": False, "message": "Payment failed"}


# PaymentMethod Class
class PaymentMethod:
    """
    Represents the method of payment.
    """
    def process_payment(self, amount):
        """
        Processes the payment for the given amount.
        
        Args:
            amount (float): The amount to be paid.
        
        Returns:
            bool: True if payment is successful, False otherwise.
        """
        return amount > 0


# UserProfile Class
class UserProfile:
    """
    Represents a user's profile.
    
    Attributes:
        delivery_address (str): The user's delivery address.
    """
    def __init__(self, delivery_address):
        """
        Initializes a UserProfile.
        
        Args:
            delivery_address (str): The delivery address.
        """
        self.delivery_address = delivery_address


# RestaurantMenu Class
class RestaurantMenu:
    """
    Represents a restaurant's menu.
    
    Attributes:
        available_items (list): List of available menu items.
    """
    def __init__(self, available_items):
        """
        Initializes a RestaurantMenu.
        
        Args:
            available_items (list): List of items.
        """
        self.available_items = available_items

    def is_item_available(self, item_name):
        """
        Checks if an item is available.
        
        Args:
            item_name (str): The name of the item.
        
        Returns:
            bool: True if available, False otherwise.
        """
        return item_name in self.available_items


# Unit tests for OrderPlacement class
class TestOrderPlacement(unittest.TestCase):
    """
    Unit tests for the OrderPlacement class.
    """
    def setUp(self):
        self.restaurant_menu = RestaurantMenu(
            available_items=["Burger", "Pizza", "Salad"])
        self.user_profile = UserProfile(delivery_address="123 Main St")
        self.cart = Cart()
        self.order = OrderPlacement(
            self.cart, self.user_profile, self.restaurant_menu)

    def test_validate_order_empty_cart(self):
        result = self.order.validate_order()
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Cart is empty")

    def test_validate_order_item_not_available(self):
        self.cart.add_item("Pasta", 15.99, 1)
        result = self.order.validate_order()
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Pasta is not available")

    def test_validate_order_success(self):
        self.cart.add_item("Burger", 8.99, 2)
        result = self.order.validate_order()
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order is valid")

    def test_confirm_order_success(self):
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()
        result = self.order.confirm_order(payment_method)
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order confirmed")
        self.assertEqual(result["order_id"], "ORD123456")

    def test_confirm_order_failed_payment(self):
        self.cart.add_item("Pizza", 12.99, 1)
        payment_method = PaymentMethod()
        with mock.patch.object(payment_method, 'process_payment', 
                                 return_value=False):
            result = self.order.confirm_order(payment_method)
            self.assertFalse(result["success"])
            self.assertEqual(result["message"], "Payment failed")


if __name__ == "__main__":
    unittest.main()
