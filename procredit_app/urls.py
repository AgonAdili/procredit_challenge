from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('signup/', views.signup, name = 'signup'),
    path('survey/', views.survey_view, name='survey'),
    path('survey/results/', views.survey_results, name='survey_results'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.dashboard, name = 'dashboard')
]