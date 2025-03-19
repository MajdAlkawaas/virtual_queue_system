from django.test import TestCase
from django.contrib.auth import get_user_model
from customers.models import Customer, User, Manager, Queue, Operator, Category

# Create your tests here.

class CustomerModelTests(TestCase):

    def setUp(self):
        "Set up test data for all test cases."
        self.customer = Customer.objects.create(
            name="Test Customer",
            contact_firstname="John",
            contact_lastname="Doe",
            email="test@example.com",
            phone_number="1234567890",
            customer_address="123 Test Street"
        )

    def test_customer_creation(self):
        "Test if customer is created successfully."
        self.assertEqual(self.customer.name, "Test Customer")
        self.assertEqual(self.customer.email, "test@example.com")

    def test_customer_str_representation(self):
        "Test the __str__ method of Customer model."
        self.assertEqual(str(self.customer), "Test Customer")

    def test_customer_email_unique(self):
        "Test that email field is unique."
        with self.assertRaises(Exception):  # Should raise IntegrityError
            Customer.objects.create(
                name="Test Customer",
                contact_firstname="Jane",
                contact_lastname="Doe",
                email="test@example.com",  # Same email as self.customer
                phone_number="0987654321",
                customer_address="456 Another Street"
            )
