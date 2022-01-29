from django.urls import path
from . import views

urlpatterns = [
    path('deviceadd/', views.deviceadd, name='deviceadd'),
    path('deviceaddconf/', views.deviceaddconf, name='deviceaddconf'),
    path('devicesaved/', views.devicesaved, name='devicesaved'),
    path('collectiveget/', views.collectiveget, name='collectiveget'),
    path('collectiveset/', views.collectiveset, name='collectiveset'),
]