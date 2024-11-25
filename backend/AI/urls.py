from django.urls import path
from . import views

urlpatterns = [
    path('summary', views.ai_summary, name='summary'),
]