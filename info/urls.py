from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('contact/', views.create_contact, name='contact'),
    path('about_us/', views.about_us, name='about_us'),
]