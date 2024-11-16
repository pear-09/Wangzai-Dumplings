from django.shortcuts import render

# Create your views here.
# folder/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .forms import CreateFolderForm
from .models import Folder
from user.utils import verify_and_refresh_token  # 自定义的 token 验证函数
from rest_framework_simplejwt.tokens import AccessToken
from django.http import QueryDict
import json
import logging
logger = logging.getLogger(__name__)

@csrf_exempt  # Disable CSRF for simplicity in this example
def create_folder_view(request):
    if request.method == 'POST':
        # Verify and refresh the token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # Get user_id from the token
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token verification failed: {str(e)}"})

        # Retrieve form data
        data = json.loads(request.body)  # 解析 JSON 数据
        form = CreateFolderForm(data)  # 使用数据来填充表单
        # form = CreateFolderForm(request.POST)

        if not form.is_valid():
            return JsonResponse({"code": 1, "msg": f"Parameter validation failed: {form.errors}"})

        # Extract validated data
        name = form.cleaned_data['name']
        folder_type = form.cleaned_data.get('folder_type', '')  # Example field for type
        parent_folder_id = form.cleaned_data.get('parent_folder_id')

        # Create a new folder
        folder = Folder(
            user_id=user_id,
            name=name,
            type=folder_type,
            parent_folder_id=parent_folder_id,
        )
        folder.save()

        # Return response with created folder details
        return JsonResponse({
            "code": 0,
            "msg": "Folder created successfully",
            "data": {
                "id": folder.id,
                "user_id": folder.user_id,
                "name": folder.name,
                "created_at": folder.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        })

    return JsonResponse({"code": 1, "msg": "Invalid request method"})

@csrf_exempt  # 禁用 CSRF 验证，便于测试和开发
def get_all_folders_view(request):
    if request.method == 'GET':
        # 验证并刷新令牌
        try:
            token = verify_and_refresh_token(request)  # 验证请求中的令牌
            access_token = AccessToken(token)  # 获取访问令牌
            user_id = access_token['user_id']  # 从令牌中提取 user_id
        except Exception as e:
            # 如果令牌验证失败，返回错误信息
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 查询用户的所有文件夹
        folders = Folder.objects.filter(user_id=user_id).order_by('created_at')

        # 准备文件夹数据
        folder_data = [{
            "id": folder.id,
            "user_id": folder.user_id,
            "name": folder.name,
            "created_at": folder.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": folder.updated_at.strftime("%Y-%m-%d %H:%M:%S") if folder.updated_at else None,
            "deleted_at": folder.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if folder.deleted_at else None
        } for folder in folders]

        # 返回包含所有文件夹详细信息的响应
        return JsonResponse({
            "code": 0,
            "msg": "success",
            "data": folder_data
        })

    # 如果请求方法不是 GET，则返回错误信息
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})


@csrf_exempt  # 禁用 CSRF 验证
def rename_folder_view(request):
    if request.method == 'PUT':
        # 验证并刷新令牌
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从令牌中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 解析 JSON 数据
        try:
            payload = json.loads(request.body.decode('utf-8'))
            folder_id = payload.get('id')  # 确保与前端字段匹配
            new_name = payload.get('name')
        except json.JSONDecodeError:
            return JsonResponse({"code": 1, "msg": "请求体不是有效的 JSON 数据"})

        # 验证文件夹 ID 和名称是否提供
        if not folder_id or not new_name:
            return JsonResponse({"code": 1, "msg": "参数缺失：需要 folder_id 和 name"})

        # 查询指定 ID 的文件夹
        try:
            folder = Folder.objects.get(id=folder_id, user_id=user_id)
        except Folder.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "文件夹不存在或无权限"})

        # 更新文件夹名称
        folder.name = new_name
        folder.save()

        # 返回更新后的文件夹信息
        return JsonResponse({
            "code": 0,
            "msg": "success",
            "data": {
                "id": folder.id,
                "user_id": folder.user_id,
                "name": folder.name,
                "created_at": folder.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": folder.updated_at.strftime("%Y-%m-%d %H:%M:%S") if folder.updated_at else None,
                "deleted_at": folder.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if folder.deleted_at else None
            }
        })

    # 如果请求方法不是 PUT，则返回错误信息
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

@csrf_exempt  # 禁用 CSRF 验证
def delete_folder_view(request):
    logger.debug("delete_folder_view called")
    if request.method == 'POST':  # 将请求方法改为 POST
        logger.debug(f"Request data: {request.POST}")
        # 验证并刷新令牌
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从令牌中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取请求中的文件夹ID
        folder_id = request.POST.get('folder_id')

        # 验证文件夹ID是否提供
        if not folder_id:
            return JsonResponse({"code": 1, "msg": "参数缺失：需要 folder_id"})

        # 查询指定 ID 的文件夹
        try:
            folder = Folder.objects.get(id=folder_id, user_id=user_id)
        except Folder.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "文件夹不存在或无权限"})

        # 删除文件夹
        folder.delete()

        # 返回删除成功的响应
        return JsonResponse({"code": 0, "msg": "success"})

    # 如果请求方法不是 POST，则返回错误信息
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})