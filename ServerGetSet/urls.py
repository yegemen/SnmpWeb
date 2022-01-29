from django.urls import path
from . import views

urlpatterns = [
    path('snmpget/', views.snmpget, name='snmpget'),
    path('snmpset/', views.snmpset, name='snmpset'),
]