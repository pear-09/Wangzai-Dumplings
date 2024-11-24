from django.db import models
import datetime


def get_created_at_default():
    return datetime.datetime.now()


def get_deleted_at_default():
    return datetime.datetime.now()


class Date(models.Model):
    id = models.IntegerField(primary_key=True)  # 自定义id字段作为主键
    user_id = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    time = models.DateTimeField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    created_at = models.DateTimeField(default=get_created_at_default)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=get_deleted_at_default)
    # 添加status字段，设置默认值为'未完成'，这里使用CharField举例，你也可以根据实际需求选择其他合适的字段类型，比如BooleanField等
    status = models.CharField(max_length=20, default='未完成')

    @classmethod
    def get_next_id(cls):
        last_date = cls.objects.order_by('-id').first()  # 获取数据库中最后一条记录（按id倒序排序后的第一条）
        if last_date:
            return last_date.id + 1
        return 1  # 如果没有记录，则从1开始

def save(self, *args, **kwargs):
        # 保持 get_created_at_default 和 get_deleted_at_default 的逻辑，确保默认值被正确赋值
        if not self.created_at:
            self.created_at = get_created_at_default()  # 确保 created_at 使用默认值
        if not self.deleted_at:
            self.deleted_at = get_deleted_at_default()  # 确保 deleted_at 使用默认值
        super(Date, self).save(*args, **kwargs)  # 调用父类的 save 方法