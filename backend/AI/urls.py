from django.urls import path
from . import views

urlpatterns = [
    path('summary', views.ai_summary, name='summary'),
    path('explain', views.ai_explain, name='explain'),
    path('keywords', views.ai_extract_keywords, name='keywords'),
    path('translate', views.ai_translate, name = 'translate'),
    path('plan', views.ai_plan, name = 'plan'),
    path('beauty', views.ai_beauty, name = 'beauty'),
    path('generate', views.ai_generate, name = 'generate'),
]