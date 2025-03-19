from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from customers.models import Manager, Operator, Customer
from customers.decorators import manager_required, operator_required
from django.http import HttpResponse

User = get_user_model()

class DecoratorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Create a customer
        self.customer = Customer.objects.create(
            name="Test Customer",
            contact_firstname="John",
            contact_lastname="Doe",
            email="test@example.com",
            phone_number="123456789",
            customer_address="123 Test Street"
        )

        # Create users
        self.manager_user = User.objects.create_user(username="manager", password="password123", is_manager=True)
        self.operator_user = User.objects.create_user(username="operator", password="password123", is_operator=True)
        self.regular_user = User.objects.create_user(username="regular", password="password123")

        # Assign manager/operator roles
        self.manager = Manager.objects.create(user=self.manager_user, customer=self.customer)
        self.operator = Operator.objects.create(user=self.operator_user, customer=self.customer, manager=self.manager)

    def test_manager_access(self):
        """Test that a manager can access a manager-required view."""
        request = self.factory.get("/")
        request.user = self.manager_user

        @manager_required
        def mock_view(request):
            return HttpResponse("Success")

        response = mock_view(request)
        self.assertEqual(response.status_code, 200)

    def test_non_manager_redirected(self):
        """Test that a non-manager is redirected."""
        request = self.factory.get("/")
        request.user = self.regular_user

        @manager_required
        def mock_view(request):
            return HttpResponse("Success")

        response = mock_view(request)
        self.assertEqual(response.status_code, 302)  # Redirect to forbidden page

    def test_operator_access(self):
        """Test that an operator can access an operator-required view."""
        request = self.factory.get("/")
        request.user = self.operator_user

        @operator_required
        def mock_view(request):
            return HttpResponse("Success")

        response = mock_view(request)
        self.assertEqual(response.status_code, 200)

    def test_non_operator_redirected(self):
        """Test that a non-operator is redirected."""
        request = self.factory.get("/")
        request.user = self.regular_user

        @operator_required
        def mock_view(request):
            return HttpResponse("Success")

        response = mock_view(request)
        self.assertEqual(response.status_code, 302)  # Redirect to forbidden page
