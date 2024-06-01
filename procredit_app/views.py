from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, IncomeForm, OutcomeForm, LoginForm, OutcomeCategoryForm
from .models import Client, NonClient, Income, Outcome, OutcomeCategory

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
    categories = OutcomeCategory.objects.filter(user=request.user)

    # Calculate total income and total outcome
    total_income = sum(income.amount for income in incomes)
    total_outcome = sum(outcome.amount for outcome in outcomes)

    # Calculate savings and debts
    savings = total_income - total_outcome
    debts = total_outcome - total_income if total_outcome > total_income else 0

    if request.method == 'POST':
        if 'income_submit' in request.POST:
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                income = income_form.save(commit=False)
                income.user = request.user
                income.save()
                return redirect('dashboard')
        elif 'outcome_submit' in request.POST:
            outcome_form = OutcomeForm(request.POST, user=request.user)
            if outcome_form.is_valid():
                outcome = outcome_form.save(commit=False)
                outcome.user = request.user
                outcome.save()
                return redirect('dashboard')
        elif 'category_submit' in request.POST:
            category_form = OutcomeCategoryForm(request.POST)
            if category_form.is_valid():
                category = category_form.save(commit=False)
                category.user = request.user
                category.save()
                return redirect('dashboard')
    else:
        income_form = IncomeForm()
        outcome_form = OutcomeForm(user=request.user)
        category_form = OutcomeCategoryForm()

    context = {
        'incomes': incomes,
        'outcomes': outcomes,
        'total_income': total_income,
        'total_outcome': total_outcome,
        'savings': savings,
        'debts': debts,
        'income_form': income_form,
        'outcome_form': outcome_form,
        'category_form': category_form,
        'categories': categories,
    }
    return render(request, 'dashboard.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')