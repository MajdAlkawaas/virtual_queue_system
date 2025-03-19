from django.test import TestCase
from customers.forms import (
    ManagerSignupForm,
    OperatorSignupForm,
    LoginForm,
    CreateQueueForm,
    ModifyQueueForm
)
from customers.models import User, Customer, Manager, Operator, Queue, Category
from django.contrib.auth import authenticate


class CustomerFormsTests(TestCase):
    def setUp(self):
        # Create a customer
        self.customer = Customer.objects.create(
            name="Test Customer",
            contact_firstname="John",
            contact_lastname="Doe",
            email="test@example.com",
            phone_number="123456789",
            customer_address="123 Test Street"
        )

        # Create manager user
        self.manager_user = User.objects.create_user(username="manager", password="password123", is_manager=True)
        self.manager = Manager.objects.create(user=self.manager_user, customer=self.customer)

        # Create operator user
        self.operator_user = User.objects.create_user(username="operator", password="password123", is_operator=True)
        self.operator = Operator.objects.create(user=self.operator_user, customer=self.customer, manager=self.manager)

    def test_manager_signup_form_valid(self):
        """Test if ManagerSignupForm is valid with correct data."""
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "manager2",
            "email": "manager2@example.com",
            "password": "securepassword"
        }
        form = ManagerSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manager_signup_creates_manager(self):
        """Test if ManagerSignupForm creates a user and assigns them as a manager."""
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "new_manager",
            "email": "new_manager@example.com",
            "password": "securepassword"
        }
        form = ManagerSignupForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.is_manager)
        self.assertTrue(Manager.objects.filter(user=user).exists())

    def test_operator_signup_form_valid(self):
        """Test if OperatorSignupForm is valid with correct data."""
        form_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "username": "operator2",
            "email": "operator2@example.com",
            "password": "securepassword"
        }
        form = OperatorSignupForm(data=form_data, user=self.manager_user)
        self.assertTrue(form.is_valid())

    def test_operator_signup_creates_operator(self):
        """Test if OperatorSignupForm creates a user and assigns them as an operator."""
        form_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "username": "new_operator",
            "email": "new_operator@example.com",
            "password": "securepassword"
        }
        form = OperatorSignupForm(data=form_data, user=self.manager_user)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.is_operator)
        self.assertTrue(Operator.objects.filter(user=user).exists())

    def test_login_form_valid(self):
        """Test if LoginForm validates correct credentials."""
        form_data = {"username": "manager", "password": "password123"}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        """Test if LoginForm rejects incorrect credentials."""
        form_data = {"username": "manager", "password": "wrongpassword"}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_create_queue_form_valid(self):
        """Test if CreateQueueForm is valid with correct data."""
        form_data = {
            "name": "New Queue",
            "operators": [self.operator.pk],
            "categories": "General, VIP"
        }
        form = CreateQueueForm(data=form_data, manager=self.manager)
        self.assertTrue(form.is_valid())

    def test_create_queue_creates_queue_and_categories(self):
        """Test if CreateQueueForm correctly creates a queue and categories."""
        form_data = {
            "name": "New Queue",
            "operators": [self.operator.pk],
            "categories": "General, VIP"
        }
        form = CreateQueueForm(data=form_data, manager=self.manager)
        self.assertTrue(form.is_valid())
        queue = form.save()
        self.assertTrue(Queue.objects.filter(name="New Queue").exists())
        self.assertEqual(queue.category_set.count(), 2)  # Two categories created

    def test_modify_queue_form_valid(self):
        """Test if ModifyQueueForm is valid with correct data."""
        queue = Queue.objects.create(name="Test Queue", active=True, manager=self.manager)
        form_data = {
            "name": "Updated Queue",
            "operators": [self.operator.pk],
            "categories": "Updated Category"
        }
        form = ModifyQueueForm(data=form_data, instance=queue, manager=self.manager)
        self.assertTrue(form.is_valid())

    def test_modify_queue_updates_queue_and_categories(self):
        """Test if ModifyQueueForm updates queue name and categories."""
        queue = Queue.objects.create(name="Test Queue", active=True, manager=self.manager)
        form_data = {
            "name": "Updated Queue",
            "operators": [self.operator.pk],
            "categories": "Updated Category"
        }
        form = ModifyQueueForm(data=form_data, instance=queue, manager=self.manager)
        self.assertTrue(form.is_valid())
        queue = form.save()
        self.assertEqual(queue.name, "Updated Queue")
        self.assertEqual(queue.category_set.count(), 1)  # One category updated

