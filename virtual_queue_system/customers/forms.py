from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User, Customer, Operator, Manager, Category, Queue

from django.db.models import Count
import random




# Manager signup form with additional fields
class ManagerSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name' , 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter email'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})

    def save(self, commit=True):
        print("HERE: form being saved")
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_manager = True
        if commit:
            user.save()
            Manager.objects.create(user=user, customer = Customer.objects.first())  # Explicitly create a Manager instance

        return user

# Operator signup form
class OperatorSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name' , 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter email'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        
        self.manager = Manager.objects.get(user=user.id)

        self.user = user


    def save(self, commit=True):
        print("HERE 01: form being saved")

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_operator = True
        if commit:
            print("HERE 02: form being saved")

            user.save()
            Operator.objects.create(user=user, 
                                    customer = Customer.objects.first(),
                                    manager=self.manager)  # Explicitly create a Manager instance
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data




class CreateQueueForm(forms.Form):
    name = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Queue Name'})
    )
    operators = forms.ModelMultipleChoiceField(
        queryset = Operator.objects.none(),                               # We will set this dynamically in __init__
        widget   = forms.SelectMultiple(attrs={'class': 'form-control'}),
        required = False
    )
    categories = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated categories'})
    )

    def __init__(self, *args, **kwargs):
        self.manager = kwargs.pop('manager', None)
        super().__init__(*args, **kwargs)

        if self.manager:
            self.fields['operators'].queryset = Operator.objects.filter(manager=self.manager)
            
            print(self.fields['operators'].queryset)
    def save(self, *args, **kwargs):
        # Ensure manager is available
        if not self.manager:
            raise ValueError("Manager must be provided to save the queue.")

        # Create Queue
        queue = Queue.objects.create(
            name    = self.cleaned_data['name'],
            manager = self.manager,
            active  = True
        )

        # Assign Operators
        operators = self.cleaned_data.get('operators', [])
        print("HERE", operators)
        queue.operator_set.set(operators)

        # # Create and Assign Categories
        # category_names = self.cleaned_data.get('categories', "").split(",")
        # for cat_name in category_names:
        #     cat_name = cat_name.strip()
        #     if cat_name:  # Avoid empty names
        #         Category.objects.create(name=cat_name, queue=queue)

        return queue
