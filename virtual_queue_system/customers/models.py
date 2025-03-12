from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.


class Customer(models.Model):
    name              = models.CharField(max_length=120)
    contact_firstname = models.CharField(max_length=50)
    contact_lastname  = models.CharField(max_length=50)
    email             = models.EmailField(max_length=250)
    phone_number      = models.CharField(max_length=50)
    customer_address  = models.CharField(max_length=100)
    created_at        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_manager   = models.BooleanField(default=False)
    is_operator  = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Custom related name to avoid conflicts
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Custom related name to avoid conflicts
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class Manager(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    customer   = models.ForeignKey(Customer, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} - Manager"


class Queue(models.Model): # CHANGE
    name       = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    active     = models.BooleanField()
    manager    = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Operator(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    customer   = models.ForeignKey(Customer, on_delete=models.CASCADE)
    manager    = models.ForeignKey(Manager, on_delete=models.CASCADE)
    queue      = models.ManyToManyField(Queue, blank=True)
    def __str__(self):
        return f"{self.user.username} - Operator"
    


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    name       = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    queue      = models.ForeignKey(Queue, on_delete=models.CASCADE) # CHANGE

    def __str__(self):
        return self.name
    