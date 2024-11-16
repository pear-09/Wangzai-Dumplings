# note/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_view, name='create'),
    path('get-all', views.get_all_view, name='get-all'),
    path('get', views.get_view, name='get'),
]
