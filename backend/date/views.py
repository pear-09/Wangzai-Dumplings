from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from.forms import CreateDateForm
from.models import Date
import datetime


@csrf_exempt
def create_view(request):
    if request.method == 'POST':
        form = CreateDateForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('user_id')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            time = form.cleaned_data.get('time')
            if not time:
                time = datetime.datetime.now()
            starttime = time
            endtime = time
            # 获取下一个可用的id
            date_id = Date.get_next_id()
            # 创建Date实例并保存到数据库
            new_date = Date(
                id=date_id,  # 设置自定义的id值
                user_id=user_id,
                title=title,
                description=description,
                time=time,
                starttime=starttime,
                endtime=endtime
            )
            new_date.save()
            return JsonResponse({"code": 0, "msg": "success"})
        else:
            return JsonResponse({"code": 1, "msg": form.errors})
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

# 获取所有日程
@csrf_exempt
def get_all_view(request):
    if request.method == 'GET':
        schedules = Date.objects.all()  # 将GetAll修改为Date
        schedule_list = []
        for schedule in schedules:
            schedule_obj = {
                "id": schedule.id,
                "title": schedule.title,
                "description": schedule.description,
                "time": schedule.time,
                # 如果Date模型没有status字段，这里可能需要根据实际情况处理
                "status": getattr(schedule,'status', None),
                "created_at": schedule.created_at.isoformat(),
                "updated_at": schedule.updated_at.isoformat(),
                "deleted_at": schedule.deleted_at.isoformat() if schedule.deleted_at else None
            }
            schedule_list.append(schedule_obj)
        return JsonResponse({
            "code": 0,
            "msg": "success",
            "data": schedule_list
        })
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})



# 获取单天日程
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from.models import Date


@csrf_exempt
def get_view(request):
    if request.method == 'GET':
        time_param = request.GET.get('time')
        if time_param:
            try:
                # 尝试将前端传来的时间参数解析为datetime对象，假设格式为 '%Y-%m-%d'（可根据实际情况调整格式字符串）
                parsed_time = datetime.datetime.strptime(time_param, '%Y-%m-%d')
                # 使用日期部分进行过滤，这里使用 __date 后缀来只匹配日期部分
                schedules = Date.objects.filter(time__date=parsed_time.date())
            except ValueError:
                return JsonResponse({"code": 1, "msg": "时间参数格式不正确"})
        else:
            # 获取当前日期
            today = datetime.date.today()
            # 使用当前日期进行过滤
            schedules = Date.objects.filter(time__date=today)

        schedule_list = []
        for schedule in schedules:
            schedule_obj = {
                "id": schedule.id,
                "title": schedule.title,
                "description": schedule.description,
                "time": schedule.time.isoformat(),  # 将时间格式化为ISO 8601字符串，方便前端处理
                "status": schedule.status,
                "created_at": schedule.created_at.isoformat(),
                "updated_at": schedule.updated_at.isoformat(),
                "deleted_at": schedule.deleted_at.isoformat() if schedule.deleted_at else None
            }
            schedule_list.append(schedule_obj)

        return JsonResponse({
            "code": 0,
            "msg": "success",
            "data": schedule_list
        })
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})