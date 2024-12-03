from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from.forms import CreateDateForm
from user.utils import verify_and_refresh_token  # 自定义的 token 验证函数
from rest_framework_simplejwt.tokens import AccessToken
import logging
from.forms import GenerateDatePlanForm
logger = logging.getLogger(__name__)
import re


@csrf_exempt
def create_view(request):
    if request.method == 'POST':
        try:
            # 1. 验证并刷新 token
            token = verify_and_refresh_token(request)  # 使用自定义函数来验证并刷新 token
            access_token = AccessToken(token)  # 解析 token
            user_id = access_token['user_id']  # 从 token 中获取 user_id

        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 2. 获取并验证表单数据
        try:
            data = json.loads(request.body)  # 解析 JSON 数据
            form = CreateDateForm(data)  # 填充表单数据

            if not form.is_valid():
                return JsonResponse({"code": 1, "msg": f"参数验证失败: {form.errors}"})

            # 3. 提取验证后的数据
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            time = form.cleaned_data.get('time') or datetime.datetime.now()  # 使用当前时间如果没有提供

            starttime = time
            endtime = time
            date_id = Date.get_next_id()  # 获取下一个可用的 ID

            # 4. 创建并保存新的 Date 实例
            new_date = Date(
                id=date_id,
                user_id=user_id,  # 使用从 token 获取的 user_id
                title=title,
                description=description,
                time=time,
                starttime=starttime,
                endtime=endtime,
                status='未完成'
            )
            new_date.save()

            # 5. 返回成功的响应
            return JsonResponse({
                "code": 0,
                "msg": "日程创建成功",
                "data": {
                    "date_id": date_id,
                    "user_id": user_id,
                    "title": title,
                    'time':time
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({"code": 1, "msg": "无效的 JSON 数据"}, status=400)
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"服务器错误: {str(e)}"}, status=500)

    return JsonResponse({"code": 1, "msg": "无效的请求方法"}, status=405)

@csrf_exempt
def get_all_view(request):
    if request.method == 'GET':
        try:
            # 1. 验证并解析 token
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)  # 解析 token
            user_id = access_token['user_id']  # 从 token 中获取 user_id

        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 2. 获取所有日程
        try:
            schedules = Date.objects.filter(user_id=user_id)  # 或者根据 user_id 过滤：Date.objects.filter(user_id=user_id)
            schedule_list = []

            for schedule in schedules:
                schedule_obj = {
                    "id": schedule.id,
                    "title": schedule.title,
                    "description": schedule.description,
                    "time": schedule.time,
                    # 如果 Date 模型没有 status 字段，这里可以根据实际情况处理
                    "status": getattr(schedule, 'status', None),
                    "created_at": schedule.created_at.isoformat(),
                    "updated_at": schedule.updated_at.isoformat(),
                    "deleted_at": schedule.deleted_at.isoformat() if schedule.deleted_at else None
                }
                schedule_list.append(schedule_obj)

            # 3. 返回成功的响应
            return JsonResponse({
                "code": 0,
                "msg": "success",
                "data": schedule_list
            })

        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"获取日程失败: {str(e)}"})

    return JsonResponse({"code": 1, "msg": "无效的请求方法"}, status=405)



# 获取单天日程
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from.models import Date


import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Date

@csrf_exempt
def get_view(request):
    if request.method == 'GET':
        try:
            # 1. 验证并刷新 token
            token = verify_and_refresh_token(request)  # 使用自定义函数来验证并刷新 token
            access_token = AccessToken(token)  # 解析 token
            user_id = access_token['user_id']  # 从 token 中获取 user_id

        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 2. 获取日期参数（如果有）
        time_param = request.GET.get('time')
        
        if time_param:
            try:
                # 尝试将前端传来的时间参数解析为 datetime 对象，假设格式为 '%Y-%m-%d'（可根据实际情况调整格式字符串）
                parsed_time = datetime.datetime.strptime(time_param, '%Y-%m-%d')
                # 输出以调试
                print(f"Received date: {parsed_time}")
                
                # 使用日期部分进行过滤，这里使用 __date 后缀来只匹配日期部分
                # 调整过滤条件，确保日期部分匹配
                schedules = Date.objects.filter(time__date=parsed_time.date(), user_id=user_id)  # 根据 user_id 过滤日程
            except ValueError:
                return JsonResponse({"code": 1, "msg": "时间参数格式不正确"})
        else:
            # 如果没有传递时间参数，默认返回当天的日程
            today = datetime.date.today()
            schedules = Date.objects.filter(time__date=today, user_id=user_id)  # 根据 user_id 过滤日程

        # 将查询结果转换为 JSON 格式
        schedule_list = []
        for schedule in schedules:
            schedule_obj = {
                "id": schedule.id,
                "title": schedule.title,
                "description": schedule.description,
                "time": schedule.time.isoformat(),  # 将时间格式化为 ISO 8601 字符串，方便前端处理
                "status": schedule.status,
                "created_at": schedule.created_at.isoformat(),
                "updated_at": schedule.updated_at.isoformat(),
                "deleted_at": schedule.deleted_at.isoformat() if schedule.deleted_at else None
            }
            schedule_list.append(schedule_obj)

        # 返回成功响应
        return JsonResponse({
            "code": 0,
            "msg": "success",
            "data": schedule_list
        })

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})


# 修改日程接口
@csrf_exempt
def modify_schedule(request):
    if request.method == 'POST':
        try:
            # 验证并解析 Token
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 获取 user_id

        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        data = json.loads(request.body)
        schedule_id = data.get('date_id')
        title = data.get('title')
        description = data.get('description')
        time = data.get('time')

        try:
            # 查找属于当前用户的日程
            schedule = Date.objects.get(id=schedule_id, user_id=user_id)

            if title:
                schedule.title = title
            if description:
                schedule.description = description
            if time:
                schedule.time = datetime.datetime.fromisoformat(time)

            schedule.save()

            return JsonResponse({
                "code": 0,
                "msg": "日程更新成功",
                "data": {
                    "id": schedule.id,
                    "title": schedule.title,
                    "description": schedule.description,
                    "time": schedule.time.isoformat(),
                    "status": schedule.status
                }
            })
        except Date.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "日程未找到或无权限"})
        except ValueError:
            return JsonResponse({"code": 1, "msg": "时间格式错误"})
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})


# 修改日程状态
@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        try:
            # 验证 Token
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 获取 user_id

        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        data = json.loads(request.body)
        schedule_id = data.get('date_id')
        status = data.get('status')  # '完成' 或 '未完成'

        if status not in ['完成', '未完成']:
            return JsonResponse({"code": 1, "msg": "状态值无效"})

        try:
            # 查找属于当前用户的日程
            schedule = Date.objects.get(id=schedule_id, user_id=user_id)
            schedule.status = status
            schedule.save()

            return JsonResponse({
                "code": 0,
                "msg": "日程状态更新成功",
                "data": {
                    "id": schedule.id,
                    "title": schedule.title,
                    "status": schedule.status
                }
            })
        except Date.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "日程未找到或无权限"})
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})


# 获取单个日程的详细信息
@csrf_exempt
def get_single_event(request):
    try:
        event_id = request.GET.get('id')  # 获取传递的 ID 参数
        event = Date.objects.get(id=event_id)  # 根据 ID 查找日程
        data = {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "time": event.time.isoformat(),  # 格式化时间
            "status": event.status
        }
        return JsonResponse({"code": 0, "msg": "成功", "data": data})
    except Date.DoesNotExist:
        return JsonResponse({"code": 1, "msg": "日程未找到"})
    except Exception as e:
        return JsonResponse({"code": 1, "msg": str(e)})

# 删除日程 
@csrf_exempt
def delete_schedule(request):
    if request.method == 'POST':
        try:
            # 验证 Token
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 获取 user_id

        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        try:
            data = json.loads(request.body)
            schedule_id = data.get('date_id')

            if not schedule_id:
                return JsonResponse({"code": 1, "msg": "未提供日程ID"})

            # 查找属于当前用户的日程
            schedule = Date.objects.get(id=schedule_id, user_id=user_id)
            schedule.delete()  # 删除日程

            return JsonResponse({"code": 0, "msg": "日程删除成功"})
        except Date.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "日程未找到或无权限"})
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"发生错误: {str(e)}"})

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

@csrf_exempt
def generate_view(request):
    if request.method == 'POST':
        try:
            # 1. 验证并刷新token
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token验证失败: {str(e)}"})

        try:
            request_body = request.body.decode('utf-8')
            # 使用正则表达式去除不可见字符和多余空格
            request_body = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]+', '', request_body)
            request_body = request_body.strip()
            form = GenerateDatePlanForm(json.loads(request_body))
            if not form.is_valid():
                return JsonResponse({"code": 1, "msg": f"参数验证失败: {form.errors}"})

            startday_str = form.cleaned_data['startday']
            # 将startday字符串转换为datetime类型
            startday = datetime.datetime.strptime(startday_str, '%Y-%m-%d')
            plan_data = form.cleaned_data['plan']

            # 在这里进行日程生成并存储到数据库的操作
            date_list = []
            for plan in plan_data:
                day_offset = plan['day']
                contents = plan['content']
                titles = plan['title']  # content 是一个字符串数组，title 是对应的标题数组

                # 正确计算日期
                time = startday + datetime.timedelta(days=day_offset - 1)

                # 遍历 content 和 title 数组中的每一项，确保每个内容项都有对应的标题项
                for content, title in zip(contents, titles):  # 使用 zip 来一一配对 content 和 title
                    date_id = Date.get_next_id()  # 获取下一个可用 ID

                    # 创建新的日程对象
                    new_date = Date(
                        id=date_id,
                        user_id=user_id,
                        title=title,  # 精简描述
                        description=content,  # 使用内容作为描述
                        time=time,  # 日期
                        starttime=time,  # 起始时间
                        endtime=time,  # 结束时间（可根据需求调整）
                        status='未完成'  # 初始状态
                    )

                    # 保存到数据库
                    new_date.save()
                    new_date_dict = model_to_dict(new_date)
                    date_list.append(new_date_dict)

            return JsonResponse({
                "code": 0,
                "msg": "日程生成并存储成功",
                "data": date_list
            })

        except json.JSONDecodeError as e:
            return JsonResponse({"code": 1, "msg": f"JSON解析错误: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"服务器错误: {str(e)}"}, status=500)

    return JsonResponse({"code": 1, "msg": "无效的请求方法"}, status=405)