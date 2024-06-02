from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('signup/', views.signup, name = 'signup'),
    path('login/', views.user_login, name = 'login'),
    path('start/', views.start_survey, name='start_survey'),
    path('logout/', views.user_logout, name='logout'),
    path('category/', views.category_list, name='category_list'),
    path('category/add_category/', views.add_category, name='add_category'),
    path('category/add_subcategory/', views.add_subcategory, name='add_subcategory'),
    path('', views.dashboard, name = 'dashboard'),
    path('dashboard_2', views.dashboard_2, name = 'dashboard_2'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('delete_subcategory/<int:pk>/', views.delete_subcategory, name='delete_subcategory'),
]