from django.contrib import admin
from .models import *

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'spending_areas', 'housing_status', 'debts', 'usual_spending', 'subscriptions', 'wants', 'created_at')
    search_fields = ('spending_areas', 'housing_status', 'debts', 'usual_spending', 'subscriptions', 'wants')
    list_filter = ('housing_status', 'created_at')



class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sum')
    inlines = [SubCategoryInline]

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'sum')


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Survey)
