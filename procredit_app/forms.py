from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from .models import Income, Outcome, OutcomeCategory


class SignUpForm(UserCreationForm):
    name = forms.CharField(required = True, max_length = 128, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    surname = forms.CharField(required = True, max_length = 128, widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    email = forms.EmailField(required = True, max_length = 128, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    date_of_birth = forms.DateField(required = True, widget = forms.DateInput(attrs = {
                                        'type': 'date',
                                        'min': '01-01-2008',
                                        'max': date.today().isoformat()
                                    }))
    is_client = forms.BooleanField(required = True, label = 'Are you already a client?')
    address = forms.CharField(max_length = 128, widget=forms.TextInput(attrs={'placeholder': 'Address'}))


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class SpendingAreasForm(forms.Form):
    spending_areas = forms.MultipleChoiceField(
        choices=[
            ('myself', 'Myself'), ('kids', 'Kids'), ('family', 'Family'), ('school', 'School'), ('other', 'Other')
        ],
        widget=forms.CheckboxSelectMultiple
    )

class HousingStatusForm(forms.Form):
    housing_status = forms.ChoiceField(
        choices=[('i_own', 'I own'), ('i_rent', 'I rent'), ('other', 'Other')],
        widget=forms.RadioSelect
    )

class DebtsForm(forms.Form):
    debts = forms.MultipleChoiceField(
        choices=[
            ('medical_bills', 'Medical bills'), ('credit_cards', 'Credit cards'), ('student_loans', 'Student loans'), ('none_apply', 'None of these apply to me')
        ],
        widget=forms.CheckboxSelectMultiple
    )

class UsualSpendingForm(forms.Form):
    usual_spending = forms.MultipleChoiceField(
        choices=[
            ('groceries', 'Groceries'), ('personal_care', 'Personal care'), ('medical_bills', 'Medical bills'), ('clothes', 'Clothes'), ('none_apply', 'None of these apply to me')
        ],
        widget=forms.CheckboxSelectMultiple
    )

class SubscriptionsForm(forms.Form):
    subscriptions = forms.MultipleChoiceField(
        choices=[
            ('internet', 'Internet'), ('phone', 'Phone'), ('music', 'Music'), ('online_classes', 'Online classes'), ('meal_delivery', 'Meal delivery'), ('none_apply', 'None of these apply to me')
        ],
        widget=forms.CheckboxSelectMultiple
    )

class WantsForm(forms.Form):
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
