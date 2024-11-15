from django.db import models

# Create your models here.
# folder/models.py
from django.db import models
from django.conf import settings

class Folder(models.Model):
    id = models.AutoField(primary_key=True)  # 主键
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 用户ID，指向用户模型
    name = models.CharField(max_length=255)  # 文件夹名称
    type = models.CharField(max_length=50)  # 文件夹类型
    parent_folder_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)  # 父文件夹ID，可以为空
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间
    deleted_at = models.DateTimeField(null=True, blank=True)  # 删除时间（逻辑删除）

    def __str__(self):
        return self.name
