from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from guests.models import Guest
from customers.models import Queue, Manager, Category, Customer

User = get_user_model()

class GuestViewsTests(TestCase):
    def setUp(self):
        # Create User for Manager
        self.user = User.objects.create_user(username="manager_user", password="password123", is_manager=True)

        # Create Customer
        self.customer = Customer.objects.create(
            name="Test Customer",
            contact_firstname="John",
            contact_lastname="Doe",
            email="johndoe@example.com",
            phone_number="1234567890",
            customer_address="123 Test St"
        )

        # Create Manager with a User
        self.manager = Manager.objects.create(user=self.user, customer=self.customer)

        # Create Queue, Category, and Guest
        self.queue = Queue.objects.create(name="Test Queue", manager=self.manager, active=True)
        self.category = Category.objects.create(name="General", queue=self.queue)
        self.guest = Guest.objects.create(
            name="Test Guest",
            phone_number="1234567890",
            customer=self.customer,
            manager=self.manager,
            queue=self.queue,
            category=self.category
        )

    def test_guest_page_loads(self):
        response = self.client.get(f"/guests/enter_queue/{self.queue.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_guest_registration(self):
        """
        Test if a guest can successfully register in a queue.
        """
        form_data = {
            "name": "New Guest",
            "phone_number": "0987654321",
            "category": self.category.id
        }
        response = self.client.post(reverse('enter_queue', args=[self.queue.id]), data=form_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        self.assertEqual(Guest.objects.count(), 2)  # One new guest should be created

    def test_queue_guest_view(self):
        """
        Test if queue dashboard loads with guest data.
        """
        response = self.client.get(reverse('queue_guest', args=[self.queue.id, self.guest.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "queue_dashboard.html")
        self.assertContains(response, "Test Guest")

    def test_refresh_queue_status(self):
        """
        Test if queue status updates return the correct JSON response.
        """
        response = self.client.get(reverse('refresh_queue_status', args=[self.guest.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("guest_name", data)
        self.assertIn("queue_name", data)
        self.assertIn("guests_ahead", data)
        self.assertIn("estimated_wait_time", data)
