from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from .models import *

class SignUpForm(UserCreationForm):
    name = forms.CharField(required = True, max_length = 128)
    surname = forms.CharField(required = True, max_length = 128)
    email = forms.EmailField(required = True, max_length = 128)
    phone_number = PhoneNumberField(blank = False)
    date_of_birth = forms.DateField(required = True, widget = forms.DateInput(attrs = {
                                        'type': 'date',
                                        'min': '01-01-2008',
                                        'max': date.today().isoformat()
                                    }))
    is_client = forms.BooleanField(required = True, label = 'Are you already a client?')
    address = forms.CharField(max_length = 128)


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    wants = forms.MultipleChoiceField(
        choices=[
            ('dining_out', 'Dining out'), ('entertainment', 'Entertainment'), ('vacation', 'Vacation'), ('hobbies', 'Hobbies'), ('new_house_car', 'New house/car'), ('gifts', 'Gifts'), ('celebrations', 'Celebrations'), ('none_apply', 'None of these apply to me')
        ],
        widget=forms.CheckboxSelectMultiple
    )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['job_title', 'amount', 'date']

class OutcomeForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=OutcomeCategory.objects.none(), empty_label="Select Category")

    class Meta:
        model = Outcome
        fields = ['category', 'amount', 'date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(OutcomeForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = OutcomeCategory.objects.filter(user=user)

class OutcomeCategoryForm(forms.ModelForm):
    class Meta:
        model = OutcomeCategory
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'sum']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'sum']

# forms.py
from django import forms

class SpendingAreasForm(forms.Form):
    SPENDING_CHOICES = [
        ('food', 'Food'),
        ('entertainment', 'Entertainment'),
        ('bills', 'Bills'),
        # Add more choices as needed
    ]
    spending_areas = forms.MultipleChoiceField(choices=SPENDING_CHOICES, widget=forms.CheckboxSelectMultiple)

class HousingStatusForm(forms.Form):
    HOUSING_CHOICES = [
        ('own', 'Own'),
        ('rent', 'Rent'),
    ]
    housing_status = forms.ChoiceField(choices=HOUSING_CHOICES, widget=forms.RadioSelect)

class DebtsForm(forms.Form):
    DEBTS_CHOICES = [
        ('mortgage', 'Mortgage'),
        ('credit_card', 'Credit Card'),
        # Add more choices as needed
    ]
    debts = forms.MultipleChoiceField(choices=DEBTS_CHOICES, widget=forms.CheckboxSelectMultiple)

class UsualSpendingForm(forms.Form):
    SPENDING_CHOICES = [
        ('groceries', 'Groceries'),
        ('transportation', 'Transportation'),
        # Add more choices as needed
    ]
    usual_spending = forms.MultipleChoiceField(choices=SPENDING_CHOICES, widget=forms.CheckboxSelectMultiple)

class SubscriptionsForm(forms.Form):
    SUBSCRIPTIONS_CHOICES = [
        ('netflix', 'Netflix'),
        ('gym', 'Gym'),
        # Add more choices as needed
    ]
    subscriptions = forms.MultipleChoiceField(choices=SUBSCRIPTIONS_CHOICES, widget=forms.CheckboxSelectMultiple)

class WantsForm(forms.Form):
    WANTS_CHOICES = [
        ('vacation', 'Vacation'),
        ('new_car', 'New Car'),
        # Add more choices as needed
    ]
    wants = forms.MultipleChoiceField(choices=WANTS_CHOICES, widget=forms.CheckboxSelectMultiple)
