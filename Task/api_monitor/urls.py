from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('endpoint/<int:endpoint_id>/', views.endpoint_detail, name='endpoint_detail'),
    path('trigger/<int:endpoint_id>/', views.trigger_manual_check, name='trigger_manual_check'),
]