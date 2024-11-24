# note/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_view, name='create'),
    path('get-all', views.get_all_view, name='get-all'),
    path('get', views.get_view, name='get'),
    path('modify', views.modify_schedule, name='modify'),
    path('status', views.update_status, name='status'),
    path('get-single', views.get_single_event, name='get-single'),
    path('delete', views.delete_schedule, name='delete'),
]
