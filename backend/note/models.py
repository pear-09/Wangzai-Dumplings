from django.core.mail.message import utf8_charset
from django.db import models
from django.conf import settings  # 导入 settings

# 标签模型
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 标签名称

    def __str__(self):
        return self.name

# 笔记模型
class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 使用 settings.AUTH_USER_MODEL 引用自定义用户模型
    title = models.CharField(max_length=255)  # 笔记标题
    content = models.TextField()  # 笔记内容
    folder_id = models.IntegerField()  # 文件夹 ID
    tags = models.ManyToManyField(Tag, blank=True)  # 多对多关系，笔记与标签关联
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间
    deleted_at = models.DateTimeField(null=True, blank=True)  # 删除时间

    def __str__(self):
        return self.title
