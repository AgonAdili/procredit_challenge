from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, IncomeForm, OutcomeForm
from .models import Client, NonClient, Income, Outcome

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_client = form.cleaned_data.get('is_client')
            if is_client:
                Client.objects.create(user = user)
            else:
                NonClient.objects.create(user = user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    pass

def dashboard(request):
    incomes = Income.objects.filter(user = request.user)
    outcomes = Outcome.objects.filter(user = request.user)
    
    context = {
        'incomes': incomes,
        'outcomes': outcomes,
    }

    return render(request, 'dashboard.html', context)