from django.contrib import admin
from .models import Survey

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'spending_areas', 'housing_status', 'debts', 'usual_spending', 'subscriptions', 'wants', 'created_at')
    search_fields = ('spending_areas', 'housing_status', 'debts', 'usual_spending', 'subscriptions', 'wants')
    list_filter = ('housing_status', 'created_at')

admin.site.register(Survey)
