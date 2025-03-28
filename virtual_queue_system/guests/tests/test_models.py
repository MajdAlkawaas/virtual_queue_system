from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from guests.models import Guest
from customers.models import Queue, Manager, Category, Customer

User = get_user_model()

class GuestViewsTests(TestCase):

    def setUp(self):
        # Create a User for the Manager
        self.user = User.objects.create(username="test_manager")

        # Create a Customer
        self.customer = Customer.objects.create(
            name="Test Customer",
            contact_firstname="John",
            contact_lastname="Doe",
            email="test@example.com",
            phone_number="1234567890",
            customer_address="123 Street"
        )

        # Create a Manager linked to the User
        self.manager = Manager.objects.create(user=self.user, customer=self.customer)

        # Create a Queue linked to the Manager
        self.queue = Queue.objects.create(name="Test Queue", manager=self.manager, active=True)

        # Create a Category linked to the Queue
        self.category = Category.objects.create(name="General", queue=self.queue)

        # Create a Guest
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
        form_data = {
            "name": "New Guest",
            "phone_number": "0987654321",
            "category": self.category.id
        }
        response = self.client.post(reverse('enter_queue', args=[self.queue.id]), data=form_data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertEqual(Guest.objects.count(), 2)  # New guest should be created

    def test_queue_guest_view(self):
        response = self.client.get(reverse('queue_guest', args=[self.queue.id, self.guest.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "queue_dashboard.html")
        self.assertContains(response, "Test Guest")

    def test_refresh_queue_status(self):
        response = self.client.get(reverse('refresh_queue_status', args=[self.guest.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("guest_name", data)
        self.assertIn("queue_name", data)
        self.assertIn("guests_ahead", data)
        self.assertIn("estimated_wait_time", data)
