from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 检查是否提供了 username 和 password
        # 检查是否提供了 username 和 password
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({"code": 1, "msg": "用户名和密码不能为空"})

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()  # 保存表单数据到数据库
            return JsonResponse({"code": 0, "msg": "success"})
        else:
            return JsonResponse({"code": 1, "msg": "注册失败", "errors": form.errors})

    
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})
