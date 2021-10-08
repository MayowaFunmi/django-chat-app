from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('add_country/', views.add_country, name='add_country'),
    path('add_city/', views.add_city, name='add_city'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_profile/', views.user_profile, name='create_profile')
]
