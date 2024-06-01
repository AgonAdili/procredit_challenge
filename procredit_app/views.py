from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from .models import *
from django.http import JsonResponse
import json


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
        'outcomes': outcomes
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

def survey_results(request):
    responses = Survey.objects.all()
    return render(request, 'survey_results.html', {'responses': responses})