import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from user.utils import verify_and_refresh_token  # 自定义的 token 验证函数
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings

@csrf_exempt
def ai_summary(request):
    if request.method == 'POST':
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"}, status=401)

        # 获取前端请求数据
        text = request.POST.get('text', '').strip()
        summary_length = request.POST.get('summary_length', None)
        AI_model = request.POST.get('AI_model', None)

        if not text:
            return JsonResponse({"code": 1, "msg": "待生成摘要的文本内容不能为空"}, status=400)

        if summary_length:
            try:
                summary_length = int(summary_length)
                if summary_length <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({"code": 1, "msg": "summary_length必须是正整数"}, status=400)
        else:
            summary_length = 150  # 默认摘要长度

        # 转换并验证 AI_model
        if AI_model is None:
            return JsonResponse({"code": 1, "msg": "请选择AI模型"}, status=400)
        
        try:
            AI_model = int(AI_model)
            if AI_model not in [0, 1]:
                raise ValueError
        except ValueError:
            return JsonResponse({"code": 1, "msg": "请选择正确的AI模型"}, status=400)
        

        # 配置API请求
        model = "gpt-4o-mini" if AI_model == 0 else "moonshot-v1-8k"
        api_url = "https://api.gptsapi.net/v1/chat/completions" if AI_model == 0 else "https://api.moonshot.cn/v1/chat/completions" 
        
        prompt = f"请为以下文本生成摘要，控制在{summary_length}个字：\n\n{text}"
        payload = {
            "messages": [
                {"role": "system", "content": "你是一个擅长生成文本摘要的助手。"},
                {"role": "user", "content": prompt}
            ],
            "model": model,
            "max_tokens": summary_length
        }
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY if AI_model == 0 else settings.KIMI_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                summary = data['choices'][0]['message']['content'].strip()
                return JsonResponse({
                    "code": 0,
                    "msg": "success",
                    "summary": summary
                })
            else:
                return JsonResponse(
                    {"code": 1, "msg": f"调用失败，状态码：{response.status_code}", "details": response.text},
                    status=response.status_code
                )
        except requests.RequestException as e:
            return JsonResponse({"code": 1, "msg": f"请求异常：{str(e)}"}, status=500)

    return JsonResponse({"code": 1, "msg": "无效的请求方法"}, status=405)
