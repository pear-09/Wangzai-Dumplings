# note/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_note_view, name='create'),
    path('update/content', views.update_note_view, name='update/content'),
]
