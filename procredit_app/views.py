from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import *
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



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
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # This starts the session for the logged-in user
                request.session['username'] = username  # Store the username in the session
                return redirect('/start/')
            else:
                form.add_error(None, 'Invalid Username or Password!')
    else:
        form = AuthenticationForm()
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
   

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard_2', {'form': form})

def add_subcategory(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = SubCategoryForm()
    return render(request, 'add_subcategory.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


# views.py
@login_required
def start_survey(request):
    if request.method == 'POST':
        forms = [
            SpendingAreasForm(request.POST),
            HousingStatusForm(request.POST),
            DebtsForm(request.POST),
            UsualSpendingForm(request.POST),
            SubscriptionsForm(request.POST),
            WantsForm(request.POST)
        ]
        
        if all(form.is_valid() for form in forms):
            survey_response = Survey.objects.create(
                user=request.user,
                spending_areas=', '.join(forms[0].cleaned_data['spending_areas']),
                housing_status=forms[1].cleaned_data['housing_status'],
                debts=', '.join(forms[2].cleaned_data['debts']),
                usual_spending=', '.join(forms[3].cleaned_data['usual_spending']),
                subscriptions=', '.join(forms[4].cleaned_data['subscriptions']),
                wants=', '.join(forms[5].cleaned_data['wants'])
            )
            link_default_categories_to_user(request.user)
            create_user_specific_subcategories(request.user, survey_response)
            return redirect('dashboard_2')
    else:
        forms = [
            SpendingAreasForm(),
            HousingStatusForm(),
            DebtsForm(),
            UsualSpendingForm(),
            SubscriptionsForm(),
            WantsForm()
        ]
        
    context = {
        'forms': forms
    }
    return render(request, 'survey.html', context)


@login_required
def dashboard_2(request):
    user_categories = Category.objects.filter(user=request.user)
    default_categories = get_default_categories()

    context = {
        'user_categories': user_categories,
        'default_categories': default_categories
    }
    return render(request, 'dashboard_2.html', context)

def link_default_categories_to_user(user):
    default_categories = {
        'Bills': [
            'Medical bills', 'Electricity', 'Gas and Fuel', 'Water', 'Garbage', 'Taxes', 'Insurance',
        ],
        'Needs': [
            'Groceries', 'Transportation', 'Healthcare', 'Clothing', 'Education', 'Savings'
        ],
        'Wants': [
            # Add subcategories as needed
        ]
    }

    for category_name, subcategories in default_categories.items():
        category, created = Category.objects.get_or_create(name=category_name, user=user)
        for subcategory_name in subcategories:
            SubCategory.objects.get_or_create(category=category, name=subcategory_name, user=user)

def get_default_categories():
    default_categories = {
        'Bills': [
            'Medical bills', 'Electricity', 'Gas and Fuel', 'Water', 'Garbage', 'Taxes', 'Insurance',
        ],
        'Needs': [
            'Groceries', 'Transportation', 'Healthcare', 'Clothing', 'Education', 'Savings'
        ],
        'Wants': [
            # Add subcategories as needed
        ]
    }

    categories = []
    for category_name, subcategories in default_categories.items():
        category = Category(name=category_name)
        category.subcategories_list = [SubCategory(name=subcategory_name) for subcategory_name in subcategories]
        categories.append(category)

    return categories

def create_user_specific_subcategories(user, survey_response):
    usual_spending_items = survey_response.usual_spending.split(', ')
    needs_category, created = Category.objects.get_or_create(name='Needs', user=user)

    for item in usual_spending_items:
        SubCategory.objects.get_or_create(category=needs_category, name=item, user=user)


def delete_category(request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('dashboard_2')

def delete_subcategory(request, pk):
        subcategory = get_object_or_404(SubCategory, pk=pk)
        subcategory.delete()
        return redirect('dashboard_2')