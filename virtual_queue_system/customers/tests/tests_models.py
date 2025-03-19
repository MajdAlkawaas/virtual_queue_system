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

    def test_missing_required_fields(self):
        """Test creating a customer without required fields fails."""
        with self.assertRaises(Exception): # should raise validation error
            Customer.objects.create(name="")  # Name is required
class UserModelTests(TestCase):

    def setUp(self):
        """Set up test data for user models."""
        self.user = User.objects.create_user(
            username="testuser",
            phone_number="9876543210",
            password="securepassword"
        )

    def test_user_creation(self):
        """Test if user is created successfully."""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.phone_number, "9876543210")
        self.assertFalse(self.user.is_manager)
        self.assertFalse(self.user.is_operator)

    def test_user_str_representation(self):
        """Test the __str__ method of User model."""
        self.assertEqual(str(self.user), "testuser")


class ManagerModelTests(TestCase):

    def setUp(self):
        """Set up a manager user and related objects."""
        self.customer = Customer.objects.create(
            name="Manager Customer",
            contact_firstname="Alice",
            contact_lastname="Smith",
            email="alice@example.com",
            phone_number="1112223333",
            customer_address="789 Manager Street"
        )
        self.manager_user = User.objects.create_user(
            username="manageruser",
            phone_number="9999999999",
            password="securepassword",
            is_manager=True
        )
        self.manager = Manager.objects.create(
            user=self.manager_user,
            customer=self.customer
        )
    def test_manager_creation(self):
        """Test if manager is created successfully."""
        self.assertEqual(self.manager.user.username, "manageruser")
        self.assertTrue(self.manager.user.is_manager)

    def test_manager_str_representation(self):
        """Test the __str__ method of Manager model."""
        self.assertEqual(str(self.manager), "manageruser - Manager")
        
    def test_manager_user_is_unique(self):
        """Test that a user cannot be assigned as a manager twice."""
        with self.assertRaises(Exception):
            Manager.objects.create(user=self.manager_user, customer=self.customer) 

class OperatorModelTests(TestCase):

    def setUp(self):
        """Set up operator-related models."""
        self.customer = Customer.objects.create(
            name="Operator Customer",
            contact_firstname="Bob",
            contact_lastname="Jones",
            email="bob@example.com",
            phone_number="6667778888",
            customer_address="987 Operator Street"
        )
        self.manager_user = User.objects.create_user(
            username="operator_manager",
            phone_number="1231231234",
            password="securepassword",
            is_manager=True
        )
        self.manager = Manager.objects.create(
            user=self.manager_user,
            customer=self.customer
        )
        self.operator_user = User.objects.create_user(
            username="testoperator",
            phone_number="5555555555",
            password="securepassword",
            is_operator=True
        )
        self.operator = Operator.objects.create(
            user=self.operator_user,
            customer=self.customer,
            manager=self.manager
        )

    def test_operator_creation(self):
        """Test if operator is created successfully."""
        self.assertEqual(self.operator.user.username, "testoperator")
        self.assertTrue(self.operator.user.is_operator)

    def test_operator_str_representation(self):
        """Test the __str__ method of Operator model."""
        self.assertEqual(str(self.operator), "testoperator - Operator")
        
    def test_operator_has_manager(self):
        """Test that an operator must belong to a manager."""
        self.assertIsNotNone(self.operator.manager)


class CategoryModelTests(TestCase):

    def setUp(self):
        """Set up category-related models."""
        self.customer = Customer.objects.create(
            name="Category Customer",
            contact_firstname="Eve",
            contact_lastname="Williams",
            email="eve@example.com",
            phone_number="4445556666",
            customer_address="345 Category Lane"
        )
        self.manager_user = User.objects.create_user(
            username="category_manager",
            phone_number="7777777777",
            password="securepassword",
            is_manager=True
        )
        self.manager = Manager.objects.create(
            user=self.manager_user,
            customer=self.customer
        )
        self.queue = Queue.objects.create(
            name="Billing Queue",
            active=True,
            manager=self.manager
        )
        self.category = Category.objects.create(
            name="Payments",
            queue=self.queue
        )

    def test_category_creation(self):
        """Test if category is created successfully."""
        self.assertEqual(self.category.name, "Payments")
        self.assertEqual(self.category.queue.name, "Billing Queue")

    def test_category_str_representation(self):
        """Test the __str__ method of Category model."""
        self.assertEqual(str(self.category), "Payments")
