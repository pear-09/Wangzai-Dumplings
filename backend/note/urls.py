# note/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_note_view, name='create'),
    path('update/content', views.update_note_view, name='update/content'),
    path('query',views.get_note_view, name='query'),
    path('query-all',views.get_notes_in_folder_view, name='query-all'),
    path('delete',views.delete_note_view, name='delete'),
    path('update/tag', views.update_note_tag_view, name='update_note_tag'),
     path('search', views.search_notes_by_tag_view, name='search_notes_by_tag'),
     path('update/title', views.update_note_title_view, name='update_note_title'),
]
