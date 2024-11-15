# note/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_note_view, name='create'),
    path('update/content', views.update_note_view, name='update/content'),
    path('query',views.get_note_view, name='query'),
    path('query-all',views.get_notes_in_folder_view, name='query-all'),
    path('delete',views.delete_note_view, name='delete'),
]
