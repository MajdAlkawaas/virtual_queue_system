from django.contrib import admin
from customers.models import Category, Operator, Queue, Manager, User, Customer
from django.contrib.auth.admin import UserAdmin
# Register your models here.




admin.site.register(User, UserAdmin)

# Registering the models with the admin site
admin.site.register(Category)
admin.site.register(Queue)

# Register Manager, Operator, and Customer if needed
admin.site.register(Manager)
admin.site.register(Operator)
admin.site.register(Customer)

