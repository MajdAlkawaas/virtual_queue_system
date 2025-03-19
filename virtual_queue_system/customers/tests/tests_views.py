from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from customers.models import Manager, Operator, Queue, Customer
from guests.models import Guest
from customers.decorators import manager_required, operator_required

User = get_user_model()

class CustomerViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

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

        # Assign manager and operator roles
        self.manager = Manager.objects.create(user=self.manager_user, customer=self.customer)
        self.operator = Operator.objects.create(user=self.operator_user, customer=self.customer, manager=self.manager)

        # Create a queue
        self.queue = Queue.objects.create(name="Test Queue", active=True, manager=self.manager)

    def test_homepage_loads(self):
        """Test if the homepage loads successfully."""
        response = self.client.get(reverse("homepage"))  # Ensure you have a URL named 'homepage'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_manager_dashboard_access(self):
        """Test if the manager can access the manager dashboard."""
        self.client.login(username="manager", password="password123")
        response = self.client.get(reverse("manager_dashboard"))  # Ensure URL name matches
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager.html")

    def test_non_manager_dashboard_redirect(self):
        """Test if a non-manager is redirected when accessing the manager dashboard."""
        self.client.login(username="regular", password="password123")
        response = self.client.get(reverse("manager_dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect expected

    def test_operator_dashboard_access(self):
        """Test if the operator can access the operator dashboard."""
        self.client.login(username="operator", password="password123")
        response = self.client.get(reverse("operator_dashboard"))  # Ensure URL name matches
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "operator.html")

    def test_non_operator_dashboard_redirect(self):
        """Test if a non-operator is redirected when accessing the operator dashboard."""
        self.client.login(username="regular", password="password123")
        response = self.client.get(reverse("operator_dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirect expected

    def test_generate_qr_code(self):
        """Test if QR code generation works."""
        self.client.login(username="manager", password="password123")
        response = self.client.get(reverse("generate_qr_code", args=[self.queue.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")  # Should return an image

    def test_login_valid_user(self):
        """Test login with valid credentials."""
        response = self.client.post(reverse("login"), {"username": "manager", "password": "password123"})
        self.assertEqual(response.status_code, 302)  # Redirect expected (to dashboard)

    def test_login_invalid_user(self):
        """Test login with invalid credentials."""
        response = self.client.post(reverse("login"), {"username": "wronguser", "password": "wrongpass"})
        self.assertEqual(response.status_code, 200)  # Stay on the login page
        self.assertContains(response, "Login failed", status_code=200)

    def test_logout_redirects_to_login(self):
        """Test if logout redirects to login page."""
        self.client.login(username="manager", password="password123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Redirect to login page
