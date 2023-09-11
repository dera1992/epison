from django.urls import path
from . import views

app_name = 'conference'

urlpatterns = [
    path('certificate/(<pk>\d+)/', views.certificate_view, name='certificate'),
    path('certificate/download/(<pk>\d+)/', views.download_certificate, name='download_certificate'),
    path('<int:id>/<slug:slug>/', views.detail_event, name='event-detail'),
    path('event-list/', views.list_event, name='event-list'),
    path('speaker-detail/(<pk>\d+)/', views.detail_speaker, name='speaker-detail'),
    path('event-register/(<pk>\d+)/', views.register_event, name='event-register'),
    path('event-gallery/', views.gallery_event, name='event-gallery'),
    path('my-event/', views.my_registered_event, name='my-event'),

]
