import unittest
from unittest import mock  # for simulating payment gateway responses


class PaymentProcessing:
    """
    Handles validation and processing of payments using different
    payment methods.

    Attributes:
        available_gateways (list): Supported payment gateways, e.g.
            "credit_card" and "paypal".
    """

    def __init__(self):
        """
        Initializes PaymentProcessing with available payment gateways.
        """
        self.available_gateways = ["credit_card", "paypal"]

    def validate_payment_method(self, payment_method, payment_details):
        """
        Validates the payment method and its details.

        Args:
            payment_method (str): The selected payment method (e.g.
                "credit_card", "paypal").
            payment_details (dict): Details required for the payment method
                (e.g. card number, expiry date).

        Returns:
            bool: True if valid; otherwise raises ValueError.

        Raises:
            ValueError: If the payment method is unsupported or details are 
                invalid.
        """
        if payment_method not in self.available_gateways:
            raise ValueError("Invalid payment method")
        if payment_method == "credit_card":
            if not self.validate_credit_card(payment_details):
                raise ValueError("Invalid credit card details")
        return True

    def validate_credit_card(self, details):
        """
        Validates credit card details.

        Args:
            details (dict): Contains "card_number", "expiry_date", and "cvv".

        Returns:
            bool: True if valid, False otherwise.
        """
        card_number = details.get("card_number", "")
        expiry_date = details.get("expiry_date", "")
        cvv = details.get("cvv", "")
        if len(card_number) != 16 or len(cvv) != 3:
            return False
        return True

    def process_payment(self, order, payment_method, payment_details):
        """
        Processes payment for an order by validating the method and
        interacting with the gateway.

        Args:
            order (dict): Order details including total amount.
            payment_method (str): The selected payment method.
            payment_details (dict): Details required for the payment method.

        Returns:
            str: Message indicating success or failure.
        """
        try:
            self.validate_payment_method(payment_method, payment_details)
            payment_response = self.mock_payment_gateway(
                payment_method, payment_details, order["total_amount"]
            )
            if payment_response["status"] == "success":
                return "Payment successful, Order confirmed"
            else:
                return "Payment failed, please try again"
        except Exception as e:
            return f"Error: {str(e)}"

    def mock_payment_gateway(self, method, details, amount):
        """
        Simulates interaction with a payment gateway.

        Args:
            method (str): Payment method (e.g. "credit_card").
            details (dict): Payment details (e.g. card number).
            amount (float): Amount to be charged.

        Returns:
            dict: Mock response indicating success or failure.
        """
        if (method == "credit_card" and
                details["card_number"] == "1111222233334444"):
            return {"status": "failure", "message": "Card declined"}
        return {"status": "success", "transaction_id": "abc123"}


class TestPaymentProcessing(unittest.TestCase):
    """
    Unit tests for PaymentProcessing.
    """
    def setUp(self):
        """
        Sets up the test environment.
        """
        self.payment_processing = PaymentProcessing()

    def test_validate_payment_method_success(self):
        """
        Test successful validation for a valid payment method.
        """
        payment_details = {
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123",
        }
        result = self.payment_processing.validate_payment_method(
            "credit_card", payment_details
        )
        self.assertTrue(result)

    def test_validate_payment_method_invalid_gateway(self):
        """
        Test validation failure for an unsupported payment method.
        """
        payment_details = {
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123",
        }
        with self.assertRaises(ValueError) as context:
            self.payment_processing.validate_payment_method(
                "bitcoin", payment_details
            )
        self.assertEqual(str(context.exception), "Invalid payment method")

    def test_validate_credit_card_invalid_details(self):
        """
        Test failure due to invalid credit card details.
        """
        payment_details = {"card_number": "1234", "expiry_date": "12/25", "cvv": "12"}
        result = self.payment_processing.validate_credit_card(payment_details)
        self.assertFalse(result)

    def test_process_payment_success(self):
        """
        Test successful payment processing with valid details.
        """
        order = {"total_amount": 100.00}
        payment_details = {
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123",
        }
        with mock.patch.object(
            self.payment_processing, "mock_payment_gateway",
            return_value={"status": "success"}
        ):
            result = self.payment_processing.process_payment(
                order, "credit_card", payment_details
            )
            self.assertEqual(result, "Payment successful, Order confirmed")

    def test_process_payment_failure(self):
        """
        Test payment failure due to a declined card.
        """
        order = {"total_amount": 100.00}
        payment_details = {
            "card_number": "1111222233334444",
            "expiry_date": "12/25",
            "cvv": "123",
        }
        with mock.patch.object(
            self.payment_processing, "mock_payment_gateway",
            return_value={"status": "failure"}
        ):
            result = self.payment_processing.process_payment(
                order, "credit_card", payment_details
            )
            self.assertEqual(result, "Payment failed, please try again")

    def test_process_payment_invalid_method(self):
        """
        Test processing failure due to an invalid payment method.
        """
        order = {"total_amount": 100.00}
        payment_details = {
            "card_number": "1234567812345678",
            "expiry_date": "12/25",
            "cvv": "123",
        }
        result = self.payment_processing.process_payment(
            order, "bitcoin", payment_details
        )
        self.assertIn("Error: Invalid payment method", result)


if __name__ == "__main__":
    unittest.main()
