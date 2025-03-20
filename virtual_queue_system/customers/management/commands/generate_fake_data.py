import random
from django.core.management.base import BaseCommand
from faker import Faker
from customers.models import Customer, User, Manager, Operator, Queue, Category

from datetime import timedelta
from django.utils.timezone import now
from guests.models import Guest



def generate_fake_data():
    fake = Faker()
    password = "defaultpassword"  # Default password for all users

    # Create Customers
    customers = []
    for _ in range(3):
        customer = Customer.objects.create(
            name=fake.company(),
            contact_firstname=fake.first_name(),
            contact_lastname=fake.last_name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            customer_address=fake.address()
        )
        customers.append(customer)
    
    managers = []
    operators = []
    
    # Create Managers (2 per customer)
    for customer in customers:
        for _ in range(2):
            user = User.objects.create_user(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                username=fake.user_name(),
                email=fake.email(),
                password=password,
                is_manager=True,
                is_active=True
            )
            manager = Manager.objects.create(user=user, customer=customer)
            managers.append(manager)
    
    # Create Operators (3 per manager)
    for manager in managers:
        for _ in range(3):
            user = User.objects.create_user(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                username=fake.user_name(),
                email=fake.email(),
                password=password,
                is_operator=True,
                is_active=True
            )
            operator = Operator.objects.create(user=user, customer=manager.customer, manager=manager)
            operators.append(operator)
    
    queues = []
    
    # Create 5 Queues (equally distributed among managers)
    for i, manager in enumerate(managers):
        queue = Queue.objects.create(
            name=f"Queue: {fake.word()} {i+1}",
            active=True,
            manager=manager
        )
        queues.append(queue)
    
    categories = []
    
    # Create 2 Categories per Queue
    for queue in queues:
        for _ in range(2):
            category = Category.objects.create(
                name=fake.word(),
                queue=queue
            )
            categories.append(category)
    
    # Assign each operator to at least one category
    for operator in operators:
        assigned_categories = random.sample(categories, random.randint(1, len(categories)))
        for category in assigned_categories:
            operator.queue.add(category.queue)
    
    print("Fake data generation complete!")

class Command(BaseCommand):
    help = "Generate fake data for customers, managers, operators, queues, and categories"

    def handle(self, *args, **kwargs):
        generate_fake_data()




def generate_fake_guest_data():
    fake = Faker()
    
    guests = []
    manager = Manager.objects.get(pk=52)
    # Get all queues
    queues = Queue.objects.filter(manager=manager)
    
    for queue in queues:
        num_guests = random.randint(5, 10)
        customer = queue.manager.customer  # Get the customer from the manager
        manager = queue.manager  # Get the manager assigned to the queue
        operators = list(Operator.objects.filter(queue=queue))  # Get operators assigned to the queue
        categories = list(Category.objects.filter(queue=queue))  # Get categories linked to the queue
        
        for i in range(1, num_guests + 1):
            walked_away = i % 6 == 0  # Every 6th guest walked away
            removed = i % 5 == 0  # Every 5th guest removed
            served = not (walked_away or removed)  # Served if not removed or walked away
            
            operator = random.choice(operators) if operators else None  # Pick a random operator if available
            category = random.choice(categories) if categories else None  # Pick a random category if available
            
            begin_time = now()
            service_time = timedelta(minutes=random.randint(2, 15))
            end_time = begin_time + service_time if served else None
            
            guest = Guest.objects.create(
                name=fake.name(),
                phone_number=fake.phone_number(),
                walked_away=walked_away,
                removed=removed,
                served=served,
                created_at=now(),
                guest_number=i,
                customer=customer,
                manager=manager,
                queue=queue,
                category=category,
                operator=operator,
                begin_of_service_time=begin_time if served else None,
                end_of_service_time=end_time if served else None
            )
            guests.append(guest)
    
    print("Fake guest data generation complete!")

class Command(BaseCommand):
    help = "Generate fake guest data"

    def handle(self, *args, **kwargs):
        generate_fake_guest_data()
