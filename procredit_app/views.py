from django.shortcuts import render, redirect
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
                return redirect('/survey/')
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
   
def survey_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Survey.objects.create(
            spending_areas=', '.join(data.get('spending_areas', [])),
            housing_status=data.get('housing_status', ''),
            debts=', '.join(data.get('debts', [])),
            usual_spending=', '.join(data.get('usual_spending', [])),
            subscriptions=', '.join(data.get('subscriptions', [])),
            wants=', '.join(data.get('wants', []))
        )
        return JsonResponse({'status': 'success'})

    forms = [
        ('Where do you spend the money?', SpendingAreasForm()),
        ('Do you own or do you rent?', HousingStatusForm()),
        ('Do you have any debts?', DebtsForm()),
        ('Where do you usually spend money?', UsualSpendingForm()),
        ('Do you have any subscriptions?', SubscriptionsForm()),
        ('What are your wants?', WantsForm()),
    ]

    return render(request, 'survey.html', {'forms': forms})

def submit_survey(request):
    if request.method == 'POST':
        spending_areas = request.POST.getlist('spending_areas')
        housing_status = request.POST.get('housing_status')
        debts = request.POST.getlist('debts')
        usual_spending = request.POST.getlist('usual_spending')
        subscriptions = request.POST.getlist('subscriptions')
        wants = request.POST.getlist('wants')

        if spending_areas and housing_status and debts and usual_spending and subscriptions and wants:
            survey = Survey(
                user=request.user,
                spending_areas=','.join(spending_areas),
                housing_status=housing_status,
                debts=','.join(debts),
                usual_spending=','.join(usual_spending),
                subscriptions=','.join(subscriptions),
                wants=','.join(wants),
            )
            survey.save()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'})
    else:
        forms = {
            'spending_areas_form': SpendingAreasForm(),
            'housing_status_form': HousingStatusForm(),
            'debts_form': DebtsForm(),
            'usual_spending_form': UsualSpendingForm(),
            'subscriptions_form': SubscriptionsForm(),
            'wants_form': WantsForm(),
        }
        return render(request, 'survey.html', {'forms': forms})

    

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
            SubCategory.objects.get_or_create(category=category, name=subcategory_name)

def survey_results(request):
    survey_responses = Survey.objects.filter(user=request.user)
    categories = Category.objects.all()  # Fetch all categories that are predefined
    return render(request, 'category_list.html', {'survey_responses': survey_responses, 'categories': categories})

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
    return render(request, 'add_category.html', {'form': form})

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
