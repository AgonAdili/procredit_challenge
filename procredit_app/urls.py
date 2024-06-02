from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('signup/', views.signup, name = 'signup'),
    path('survey/', views.survey_view, name='survey'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.dashboard, name = 'dashboard'),
    path('savings/', views.savings, name = 'savings'),
    path('investing/', views.investing, name = 'investing')
]