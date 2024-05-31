from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from .models import Income, Outcome


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
        fields = ('password1', 'password2')


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['job_title', 'amount', 'date']


class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['category', 'amount', 'date']