from django.test import TestCase
from guests.forms import GuestForm
from customers.models import Category

class GuestFormTests(TestCase):

    def setUp(self):
        """Create test data for categories."""
        self.category = Category.objects.create(name="Test Category", queue=None)

    def test_guest_form_valid_data(self):
        """Test form with valid data should be valid."""
        form_data = {
            "name": "John Doe",
            "phone_number": "1234567890",
            "category": self.category.id
        }
        form = GuestForm(data=form_data, categories=[self.category])
        self.assertTrue(form.is_valid())

    def test_guest_form_missing_name(self):
        """Test form is invalid when name is missing."""
        form_data = {
            "phone_number": "1234567890",
            "category": self.category.id
        }
        form = GuestForm(data=form_data, categories=[self.category])
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_guest_form_missing_phone_number(self):
        """Test form is invalid when phone number is missing."""
        form_data = {
            "name": "John Doe",
            "category": self.category.id
        }
        form = GuestForm(data=form_data, categories=[self.category])
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)

    def test_guest_form_invalid_category(self):
        """Test form raises validation error for non-existent category."""
        form_data = {
            "name": "John Doe",
            "phone_number": "1234567890",
            "category": 999  # Non-existent category
        }
        form = GuestForm(data=form_data, categories=[self.category])
        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)

    def test_guest_form_category_choices(self):
        """Test that category choices are correctly set."""
        form = GuestForm(categories=[self.category])
        expected_choices = [(self.category.id, str(self.category))]
        self.assertEqual(form.fields["category"].choices, expected_choices)

    def test_guest_form_widget_attributes(self):
        """Test that widgets have correct attributes."""
        form = GuestForm(categories=[self.category])
        self.assertEqual(form.fields["name"].widget.attrs["placeholder"], "Enter name")
        self.assertEqual(form.fields["phone_number"].widget.attrs["placeholder"], "Enter phone number")
        self.assertEqual(form.fields["name"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["phone_number"].widget.attrs["class"], "form-control")
