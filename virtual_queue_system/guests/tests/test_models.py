from django.test import TestCase
from django.utils.timezone import now
from guests.models import Guest, Music
from customers.models import Customer, Manager, Queue, Operator, Category, User

class GuestModelTests(TestCase):

    def setUp(self):
        """Set up required objects before each test"""
        self.customer = Customer.objects.create(
            name="Test Customer",
            contact_firstname="John",
            contact_lastname="Doe",
            email="test@example.com",
            phone_number="1234567890",
            customer_address="123 Test Street"
        )

        self.manager_user = User.objects.create_user(
            username="manager1",
            phone_number="9876543210",
            password="securepassword",
            is_manager=True
        )
        self.manager = Manager.objects.create(user=self.manager_user, customer=self.customer)

        self.queue = Queue.objects.create(name="Support Queue", active=True, manager=self.manager)

        self.operator_user = User.objects.create_user(
            username="operator1",
            phone_number="5555555555",
            password="securepassword",
            is_operator=True
        )
        self.operator = Operator.objects.create(user=self.operator_user, customer=self.customer, manager=self.manager)

        self.category = Category.objects.create(name="Billing Issues", queue=self.queue)

        self.guest = Guest.objects.create(
            name="Guest 1",
            phone_number="1112223333",
            walked_away=False,
            removed=False,
            served=False,
            guest_number=1,
            customer=self.customer,
            manager=self.manager,
            queue=self.queue,
            category=self.category,
            operator=self.operator,
            begin_of_service_time=now(),
            end_of_service_time=now()
        )

    def test_guest_creation(self):
        """Test if the guest object is created successfully"""
        self.assertEqual(self.guest.name, "Guest 1")
        self.assertEqual(self.guest.phone_number, "1112223333")
        self.assertFalse(self.guest.walked_away)
        self.assertFalse(self.guest.removed)
        self.assertFalse(self.guest.served)

    def test_guest_str_representation(self):
        """Test the __str__ method of Guest model"""
        self.assertEqual(str(self.guest), f"{self.guest.id} - Guest 1")

    def test_guest_defaults(self):
        """Test default values of Guest model fields"""
        guest = Guest.objects.create(
            name="Guest 2",
            phone_number="4445556666",
            customer=self.customer,
            manager=self.manager,
            queue=self.queue,
            category=self.category,
            operator=self.operator
        )
        self.assertFalse(guest.walked_away)
        self.assertFalse(guest.removed)
        self.assertFalse(guest.served)
        self.assertIsNone(guest.begin_of_service_time)
        self.assertIsNone(guest.end_of_service_time)

    def test_guest_foreign_keys(self):
        """Test if foreign keys are correctly set"""
        self.assertEqual(self.guest.customer, self.customer)
        self.assertEqual(self.guest.manager, self.manager)
        self.assertEqual(self.guest.queue, self.queue)
        self.assertEqual(self.guest.category, self.category)
        self.assertEqual(self.guest.operator, self.operator)
    
    def test_guest_number_auto_increment(self):
        """Test if guest_number increments correctly for new guests."""
        guest2 = Guest.objects.create(
            name="Guest 2",
            phone_number="4445556666",
            customer=self.customer,
            manager=self.manager,
            queue=self.queue,
            category=self.category,
            operator=self.operator
        )
        self.assertGreater(guest2.guest_number, self.guest.guest_number)
        
    def test_guest_queue_integrity(self):
        """Test that a guest cannot belong to multiple queues at the same time."""
        new_queue = Queue.objects.create(name="Another Queue", active=True, manager=self.manager)
        
        with self.assertRaises(Exception):  # Should raise IntegrityError if enforced at DB level
            Guest.objects.create(
                name="Guest 3",
                phone_number="7778889999",
                customer=self.customer,
                manager=self.manager,
                queue=new_queue,  # Different queue
                category=self.category,
                operator=self.operator
            )
            
    def test_guest_served_status(self):
        """Test that serving a guest updates the served status and service time."""
        self.guest.served = True
        self.guest.begin_of_service_time = now()
        self.guest.save()

        self.assertTrue(self.guest.served)
        self.assertIsNotNone(self.guest.begin_of_service_time)



class MusicModelTests(TestCase):

    def setUp(self):
        """Set up test music entry"""
        self.song = Music.objects.create(song_name="Test Song", song_url="https://example.com/song.mp3")

    def test_music_creation(self):
        """Test if a music object is created successfully"""
        self.assertEqual(self.song.song_name, "Test Song")
        self.assertEqual(self.song.song_url, "https://example.com/song.mp3")

    def test_music_str_representation(self):
        """Test the __str__ method of Music model"""
        self.assertEqual(str(self.song), "Test Song")
