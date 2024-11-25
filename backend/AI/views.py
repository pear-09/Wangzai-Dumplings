import json
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
        length = request.POST.get('length', None)
        AI_model = request.POST.get('AI_model', None)

        if not text:
            return JsonResponse({"code": 1, "msg": "待生成摘要的文本内容不能为空"}, status=400)

        if length:
            try:
                length = int(length)
                if length <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({"code": 1, "msg": "length必须是正整数"}, status=400)
        else:
            length = 150  # 默认摘要长度

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
        
        prompt = f"请为以下文本生成摘要，控制在{length}个字：\n\n{text}"
        payload = {
            "messages": [
                {"role": "system", "content": "你是一个擅长生成文本摘要的助手。"},
                {"role": "user", "content": prompt}
            ],
            "model": model,
            "max_tokens": length
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

@csrf_exempt
def ai_explain(request):
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
        length = request.POST.get('length', None)
        AI_model = request.POST.get('AI_model', None)

        if not text:
            return JsonResponse({"code": 1, "msg": "待生成摘要的文本内容不能为空"}, status=400)

        if length:
            try:
                length = int(length)
                if length <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({"code": 1, "msg": "length必须是正整数"}, status=400)
        else:
            length = 150  # 默认摘要长度

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
        
        prompt = f"请为以下文本进行解释，控制在{length}个字：\n\n{text}"
        payload = {
            "messages": [
                {"role": "system", "content": "你是一个擅长解释的助手。"},
                {"role": "user", "content": prompt}
            ],
            "model": model,
            "max_tokens": length
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

@csrf_exempt
def ai_extract_keywords(request):
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
        AI_model = request.POST.get('AI_model', None)

        if not text:
            return JsonResponse({"code": 1, "msg": "待提取关键词的文本内容不能为空"}, status=400)

        # 转换并验证 AI_model
        if AI_model is None:
            return JsonResponse({"code": 1, "msg": "请选择 AI 模型"}, status=400)
        
        try:
            AI_model = int(AI_model)
            if AI_model not in [0, 1]:
                raise ValueError
        except ValueError:
            return JsonResponse({"code": 1, "msg": "请选择正确的 AI 模型"}, status=400)
        
        # 配置API请求
        model = "gpt-4o-mini" if AI_model == 0 else "moonshot-v1-8k"
        api_url = "https://api.gptsapi.net/v1/chat/completions" if AI_model == 0 else "https://api.moonshot.cn/v1/chat/completions" 
        
        prompt = f"请从以下文本中提取几个关键词，用数组的形式返回：\n\n{text}"
        payload = {
            "messages": [
                {"role": "system", "content": "你是一个擅长提取关键词的助手。"},
                {"role": "user", "content": prompt}
            ],
            "model": model,
            "max_tokens": 150  # 适当调整 max_tokens 以适应关键词提取
        }
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY if AI_model == 0 else settings.KIMI_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # 假设AI返回的是一个 JSON 数组字符串，需要解析为实际数组
                keywords_text = data['choices'][0]['message']['content'].strip()
                
                # 尝试从文本中提取关键词数组
                try:
                    # 如果返回的是 JSON 格式的数组
                    keywords = json.loads(keywords_text)
                    if not isinstance(keywords, list):
                        raise ValueError
                except json.JSONDecodeError:
                    # 如果返回的是逗号分隔的字符串，则手动分割
                    keywords = [kw.strip() for kw in keywords_text.split(',')]
                
                return JsonResponse({
                    "code": 0,
                    "msg": "success",
                    "keywords": keywords
                })
            else:
                return JsonResponse(
                    {"code": 1, "msg": f"调用失败，状态码：{response.status_code}", "details": response.text},
                    status=response.status_code
                )
        except requests.RequestException as e:
            return JsonResponse({"code": 1, "msg": f"请求异常：{str(e)}"}, status=500)

    return JsonResponse({"code": 1, "msg": "无效的请求方法"}, status=405)

@csrf_exempt
def ai_translate(request):
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
        language = request.POST.get('language','中文')
        AI_model = request.POST.get('AI_model', None)

        if not text:
            return JsonResponse({"code": 1, "msg": "待生成摘要的文本内容不能为空"}, status=400)

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
        
        prompt = f"请将以下文本翻译成{language}：\n\n{text}"
        payload = {
            "messages": [
                {"role": "system", "content": "你是一个擅长翻译的助手。"},
                {"role": "user", "content": prompt}
            ],
            "model": model,
            "max_tokens": 2000
        }
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY if AI_model == 0 else settings.KIMI_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                translation = data['choices'][0]['message']['content'].strip()
                return JsonResponse({
                    "code": 0,
                    "msg": "success",
                    "translation": translation
                })
            else:
                return JsonResponse(
                    {"code": 1, "msg": f"调用失败，状态码：{response.status_code}", "details": response.text},
                    status=response.status_code
                )
        except requests.RequestException as e:
            return JsonResponse({"code": 1, "msg": f"请求异常：{str(e)}"}, status=500)

    return JsonResponse({"code": 1, "msg": "无效的请求方法"}, status=405)

@csrf_exempt
def ai_plan(request):
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
        days = request.POST.get('days','7')
        length = request.POST.get('length',None)
        AI_model = request.POST.get('AI_model', None)
        degree = request.POST.get('degree',None)

        if not text:
            return JsonResponse({"code": 1, "msg": "待生成摘要的文本内容不能为空"}, status=400)

        if length:
            try:
                length = int(length)
                if length <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({"code": 1, "msg": "length必须是正整数"}, status=400)
        else:
            length = 150  # 默认摘要长度

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
        
        prompt = f"请为以下文本生成{days}的{degree}复习计划，字数在{length}以内，只返回纯文本，不要加粗等等：\n\n{text}"
        payload = {
            "messages": [
                {"role": "system", "content": "你是一个擅长生成计划的助手。"},
                {"role": "user", "content": prompt}
            ],
            "model": model,
            "max_tokens": length
        }
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY if AI_model == 0 else settings.KIMI_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                translation = data['choices'][0]['message']['content'].strip()
                return JsonResponse({
                    "code": 0,
                    "msg": "success",
                    "translation": translation
                })
            else:
                return JsonResponse(
                    {"code": 1, "msg": f"调用失败，状态码：{response.status_code}", "details": response.text},
                    status=response.status_code
                )
        except requests.RequestException as e:
            return JsonResponse({"code": 1, "msg": f"请求异常：{str(e)}"}, status=500)

    return JsonResponse({"code": 1, "msg": "无效的请求方法"}, status=405)

@csrf_exempt
def ai_beauty(request):
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
        AI_model = request.POST.get('AI_model', None)

        if not text:
            return JsonResponse({"code": 1, "msg": "待生成摘要的文本内容不能为空"}, status=400)

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
        
        prompt = f"请美化以下文本：\n\n{text}"
        payload = {
            "messages": [
                {"role": "system", "content": "你是一个擅长写作的助手。"},
                {"role": "user", "content": prompt}
            ],
            "model": model,
            "max_tokens": 2000
        }
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY if AI_model == 0 else settings.KIMI_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                translation = data['choices'][0]['message']['content'].strip()
                return JsonResponse({
                    "code": 0,
                    "msg": "success",
                    "translation": translation
                })
            else:
                return JsonResponse(
                    {"code": 1, "msg": f"调用失败，状态码：{response.status_code}", "details": response.text},
                    status=response.status_code
                )
        except requests.RequestException as e:
            return JsonResponse({"code": 1, "msg": f"请求异常：{str(e)}"}, status=500)

    return JsonResponse({"code": 1, "msg": "无效的请求方法"}, status=405)
