from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, IncomeForm, OutcomeForm, LoginForm
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid Username or Password!')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url = '/login/')
def dashboard(request):
    incomes = Income.objects.filter(user=request.user)
    outcomes = Outcome.objects.filter(user=request.user)
    
    total_income = sum(income.amount for income in incomes)
    total_outcome = sum(outcome.amount for outcome in outcomes)
    savings = total_income - total_outcome
    debts = total_outcome - total_income if total_outcome > total_income else 0

    context = {
        'incomes': incomes,
        'outcomes': outcomes,
        'savings': savings,
        'debts': debts,
    }
    return render(request, 'dashboard.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')