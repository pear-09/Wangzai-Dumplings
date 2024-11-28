from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CreateNoteForm
from .forms import UpdateNoteForm
from .forms import NoteQueryForm
from .forms import FolderQueryForm
from .models import Note, Tag
from user.utils import verify_and_refresh_token  # 自定义的 token 验证函数
from rest_framework_simplejwt.tokens import AccessToken
import json

@csrf_exempt
def create_note_view(request):
    if request.method == 'POST':
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取前端请求数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        folder_id = request.POST.get('folder_id')
        tag_names = request.POST.getlist('tags')  # 获取标签名称列表

        if not title:
            title = '新建笔记'

        if not folder_id:
            return JsonResponse({"code": 1, "msg": "所属文件夹不能为空"})

        # 将标签名称转换为标签 ID 列表
        tag_ids = []
        for tag_name in tag_names:
            try:
                tag = Tag.objects.get(name=tag_name)  # 查找标签名称对应的标签实例
                tag_ids.append(tag.id)  # 将标签 ID 加入列表
            except Tag.DoesNotExist:
                tag = Tag.objects.create(name=tag_name)
                tag_ids.append(tag.id)

        # 构建包含所有字段数据的字典
        note_data = {
            'title': title,
            'content': content,
            'folder_id': folder_id,
            'tags': tag_ids  # 传递标签 ID 列表
        }

        # 创建 Note 表单实例并传入数据
        form = CreateNoteForm(note_data)

        if form.is_valid():
            # 保存笔记时，先不要提交到数据库
            note = form.save(commit=False)
            note.user_id = user_id  # 将当前用户关联到笔记
            note.title = title
            note.save()  # 保存笔记实例

            # 关联标签到笔记
            note.tags.set(tag_ids)  # 使用 set() 方法将标签关联到笔记

            # 返回成功的响应
            return JsonResponse({
                "code": 0,
                "msg": "success",
                "data": {
                    "id": note.id,
                    "user_id": note.user_id,
                    "title": note.title,
                    "content": note.content,
                    "folder_id": note.folder_id,
                    "tags": [tag.name for tag in note.tags.all()],  # 返回标签的名称
                    "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": note.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "deleted_at": note.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if note.deleted_at else None
                }
            })
        else:
            return JsonResponse({"code": 1, "msg": f"创建笔记失败: {form.errors}"})

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})


@csrf_exempt  # 禁用 CSRF 验证
def update_note_view(request):
    if request.method == 'POST':
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取前端提交的表单数据
        form = UpdateNoteForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"code": 1, "msg": f"参数验证失败: {form.errors}"})

        # 获取验证后的数据
        note_id = form.cleaned_data['note_id']
        content = form.cleaned_data['content']

        # 获取指定 ID 的笔记
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "笔记不存在"})

        # 检查是否为当前用户的笔记
        if note.user_id != user_id:
            return JsonResponse({"code": 1, "msg": "您没有权限修改此笔记"})

        # 更新笔记内容
        note.content = content
        note.save()

        # 返回更新后的笔记信息
        return JsonResponse({
            "code": 0,
            "msg": "笔记更新成功",
            "data": {
                "id": note.id,
                "user_id": note.user_id,
                "title": note.title,
                "content": note.content,
                "folder_id": note.folder_id,
                "tags": [tag.name for tag in note.tags.all()],
                "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": note.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "deleted_at": note.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if note.deleted_at else None
            }
        })

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

def get_note_view(request):
    if request.method == 'GET':
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取 query 参数，并进行表单验证
        form = NoteQueryForm(request.GET)
        if not form.is_valid():
            return JsonResponse({"code": 1, "msg": f"参数验证失败: {form.errors}"})

        # 获取验证后的数据
        note_id = form.cleaned_data['note_id']

        # 获取指定 ID 的笔记
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "笔记不存在"})

        # 检查是否为当前用户的笔记
        if note.user_id != user_id:
            return JsonResponse({"code": 1, "msg": "您没有权限查看此笔记"})

        # 返回笔记内容
        return JsonResponse({
            "code": 0,
            "msg": "笔记获取成功",
            "data": {
                "id": note.id,
                "user_id": note.user_id,
                "title": note.title,
                "content": note.content,
                "folder_id": note.folder_id,
                "tags": [tag.name for tag in note.tags.all()],
                "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": note.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "deleted_at": note.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if note.deleted_at else None
            }
        })

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

@csrf_exempt
def get_notes_in_folder_view(request):
    if request.method == 'GET':
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取 query 参数并进行表单验证
        form = FolderQueryForm(request.GET)
        if not form.is_valid():
            return JsonResponse({"code": 1, "msg": f"参数验证失败: {form.errors}"})

        # 获取验证后的数据
        folder_id = form.cleaned_data['folder_id']

        # 获取当前文件夹下所有的笔记
        notes = Note.objects.filter(user_id=user_id, folder_id=folder_id)

        # 构建响应数据
        notes_data = [
            {
                "id": note.id,
                "user_id": note.user_id,
                "title": note.title,
                "folder_id": note.folder_id,
                "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "tag": [tag.name for tag in note.tags.all()],
            }
            for note in notes
        ]

        # 返回笔记列表
        return JsonResponse({
            "code": 0,
            "msg": "success",
            "data": notes_data
        })

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

@csrf_exempt
def delete_note_view(request):
    if request.method == 'POST':
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取前端提交的 note_id
        note_id = request.POST.get('note_id')
        if not note_id:
            return JsonResponse({"code": 1, "msg": "笔记 ID 为必填项"})

        # 获取指定 ID 的笔记
        try:
            note = Note.objects.get(id=note_id, user_id=user_id)
        except Note.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "笔记不存在或无权限删除"})

        # 删除笔记
        note.delete()

        # 返回删除成功的响应
        return JsonResponse({"code": 0, "msg": "笔记删除成功"})

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

@csrf_exempt 
def update_note_tag_view(request):
    if request.method == 'POST':  # 使用 POST 方法
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取前端提交的数据
        note_id = request.POST.get('note_id')  # 获取笔记 ID
        tag_names = request.POST.getlist('tag')  # 获取标签名称列表（多个标签）

        # 验证必要参数
        if not note_id or not tag_names:
            return JsonResponse({"code": 1, "msg": "参数缺失：需要 note_id 和 tag"})

        # 查询指定的笔记
        try:
            note = Note.objects.get(id=note_id, user_id=user_id)
        except Note.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "笔记不存在或无权限修改"})

        # 清空现有标签
        note.tags.clear()

        # 查询或创建标签并添加到笔记
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())  # 清除多余空格
            note.tags.add(tag)

        # 构建响应数据
        note_data = {
            "id": note.id,
            "user_id": note.user_id,
            "title": note.title,
            "content": note.content,
            "tags": [tag.name for tag in note.tags.all()],  # 返回标签列表
            "folder_id": note.folder_id,
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": note.updated_at.strftime("%Y-%m-%d %H:%M:%S") if note.updated_at else None,
            "deleted_at": note.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if note.deleted_at else None,
        }

        # 返回成功响应
        return JsonResponse({"code": 0, "msg": "标签更新成功", "data": note_data})

    # 如果请求方法不是 POST，则返回错误信息
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})



@csrf_exempt
def search_notes_by_tag_view(request):
    if request.method == 'GET':
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取参数
        tag_name = request.GET.get('tag')
        if not tag_name:
            return JsonResponse({"code": 1, "msg": "参数缺失：需要 tag"})

        # 处理分页参数
        def get_int_param(param_value, default_value):
            try:
                return int(param_value) if param_value else default_value
            except ValueError:
                return default_value

        limit = get_int_param(request.GET.get('limit'), 10)
        offset = get_int_param(request.GET.get('offset'), 0)

        try:
            tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "标签不存在"})

        notes = Note.objects.filter(user_id=user_id, tags=tag).order_by('-created_at')[offset:offset+limit]

        notes_data = [
            {
                "id": note.id,
                "user_id": note.user_id,
                "title": note.title,
                "content": note.content,
                "folder_id": note.folder_id,
                "tag": tag_name,
                "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": note.updated_at.strftime("%Y-%m-%d %H:%M:%S") if note.updated_at else None,
                "deleted_at": note.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if note.deleted_at else None,
            }
            for note in notes
        ]

        return JsonResponse({
            "code": 0,
            "msg": "success",
            "data": {
                "notes": notes_data,
            }
        })

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

@csrf_exempt  # 禁用 CSRF 验证
def update_note_title_view(request):
    if request.method == 'POST':
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取前端提交的数据
        note_id = request.POST.get('note_id')  # 获取笔记 ID
        title = request.POST.get('title')  # 获取笔记标题

        # 验证必要参数
        if not note_id or not title:
            return JsonResponse({"code": 1, "msg": "参数缺失：需要 note_id 和 title"})

        # 查询指定 ID 的笔记
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "笔记不存在"})

        # 检查是否为当前用户的笔记
        if note.user_id != user_id:
            return JsonResponse({"code": 1, "msg": "您没有权限修改此笔记"})

        # 更新笔记标题
        note.title = title
        note.save()

        # 返回更新后的笔记信息
        return JsonResponse({
            "code": 0,
            "msg": "success",
            "data": {
                "id": note.id,
                "user_id": note.user_id,
                "title": note.title,
                "content": note.content,
                "folder_id": note.folder_id,
                "tags": [tag.name for tag in note.tags.all()],
                "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": note.updated_at.strftime("%Y-%m-%d %H:%M:%S") if note.updated_at else None,
                "deleted_at": note.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if note.deleted_at else None,
            }
        })

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})
