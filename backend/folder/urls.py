# folders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_folder_view, name='create'),
    path('get-all', views.get_all_folders_view, name='get_all'),  # 获取所有文件夹
    path('rename', views.rename_folder_view, name='rename'),  # 重命名文件夹
    path('delete', views.delete_folder_view, name='delete'),  # 删除文件夹
]
