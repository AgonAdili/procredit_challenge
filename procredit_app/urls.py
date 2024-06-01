from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.login, name = 'login'),
    path('survey/', views.survey_view, name='survey'),
    path('survey/results/', views.survey_results, name='survey_results'),

]