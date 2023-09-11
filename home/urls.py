from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

]