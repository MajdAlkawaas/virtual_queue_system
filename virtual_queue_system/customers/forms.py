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




class CreateQueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = ['name', 'operators', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'queue-name'}),
        }

    name = forms.CharField(
        widget   = forms.TextInput(attrs={'placeholder': 'Enter Queue Name', 'class':'form-control'}),
        required = False,
        label    = "Queue  Name"
    )

    operators = forms.MultipleChoiceField(
        choices  = [],
        widget   = forms.CheckboxSelectMultiple, # Optional: Checkbox UI instead of dropdown
        required = False,
        label    = "Assign Operators"
        
    )

    categories = forms.CharField(
        widget   = forms.TextInput(attrs={'placeholder': 'Comma separated categories', 'class':'form-control'}),
        required = False,
        label    = "Categories"
    )


    def __init__(self, *args, **kwargs):
        manager = kwargs.pop('manager', None)

        super().__init__(*args, **kwargs)
        self.fields['operators'].choices = [(op.pk, op.user.username) for op in Operator.objects.filter(manager=manager)]  # Update choices dynamically
    
    
class ModifyQueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = ['name', 'operators', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'queue-name'}),
        }

    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Queue Name', 'class':'form-control'}),
        required=True,
        label="Queue Name"
    )

    operators = forms.MultipleChoiceField(
        choices=[],  # Will be set dynamically in __init__
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Operators"
    )

    categories = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Comma separated categories', 'class':'form-control'}),
        required=False,
        label="Categories"
    )

    def __init__(self, *args, **kwargs):
        manager = kwargs.pop('manager', None)
        super().__init__(*args, **kwargs)

        # Get all operators under the current manager
        self.fields['operators'].choices = [(op.pk, op.user.username) for op in Operator.objects.filter(manager=manager)]

        # Pre-fill selected operators
        if self.instance and self.instance.pk:
            self.fields['operators'].initial = [op.pk for op in self.instance.operator_set.all()]

        # Pre-fill categories as a comma-separated string
        if self.instance and self.instance.pk:
            self.fields['categories'].initial = ", ".join(self.instance.category_set.values_list('name', flat=True))
     
