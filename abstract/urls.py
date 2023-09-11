from django.urls import path
from . import views

app_name = 'abstract'

urlpatterns = [
    path('abstract-list/', views.list_abstract, name='abstract-list'),
    path('create-abstract/', views.create_abstract, name='create-abstract'),
    path('edit-abstract/(<pk>\d+)/', views.edit_abstract, name='edit-abstract'),
    path('delete-abstract/(<pk>\d+)/', views.delete_abstract, name='delete-abstract'),
    path('my-abstract/', views.my_abstract, name='my-abstract'),
    path('abstract-detail/(<pk>\d+)/', views.detail_abstract, name='abstract-detail'),

]