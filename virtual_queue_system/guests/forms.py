from django import forms
from guests.models import Guest
from customers.models import Category


class GuestForm(forms.ModelForm):

    # categories = forms.ChoiceField(widget=forms.Select(attrs={'name': 'category'}))  # Define Location as a choice field

    class Meta:
        model = Guest
        fields = ['name', 'phone_number', 'category']  # Specify desired fields

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', None)
        # locations = kwargs.pop('locations', None)  # Get locations queryset
        super().__init__(*args, **kwargs)          # Initialize superclass
        
        # Customize widgets for each field

        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter name'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter phone number'})

        # self.fields['phone_number'].widget = forms.TextInput(attrs={'name': 'phone_number'})
       
        
        # Set choices for Location field if locations are provided
        if categories:
            self.fields['category'].choices = [(category.id, str(category)) for category in categories]  # Convert queryset to ID-label pairs


        print(f"HERE: {self.fields['name']}\n{self.fields['phone_number']}\n{self.fields['category'].choices}")
    def clean_category(self):
        category_id = self.cleaned_data['category'].id
        print("HERE: clean_cat")
        try:
            # Retrieve the Location object and return it
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise forms.ValidationError("This location does not exist.")