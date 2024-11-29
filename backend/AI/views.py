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
            "max_tokens": length + 100
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

        length = min(length, 2000)

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
            "max_tokens": length + 100
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

        text = request.POST.get('text', '').strip()
        days = request.POST.get('days', '7')
        AI_model = request.POST.get('AI_model', None)
        degree = request.POST.get('degree', None)

        days = int(days)
        # 验证必填字段
        if not text:
            return JsonResponse({"code": 1, "msg": "待生成计划的文本内容不能为空"}, status=400)

        # 验证 degree
        if degree:
            allowed_degrees = ['low', 'medium', 'high']
            if degree not in allowed_degrees:
                return JsonResponse({"code": 1, "msg": f"degree必须是以下值之一: {', '.join(allowed_degrees)}"}, status=400)
        else:
            degree = 'medium'  # 默认详细程度

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

        # 根据 degree 设置详细程度指令
        degree_instruction = {
            'low': '保持计划简洁，每天列出1-2个主要任务。',
            'medium': '详细列出每天的任务，每天包含2-4个具体计划项。',
            'high': '非常详细地列出每天的任务，每天包含4-6个具体计划项，并提供必要的说明。'
        }

        # 调整提示词，仅包含必要的信息，并包含 degree_instruction
        user_prompt = (
            f"生成一个为期{min(days,14)}天的复习计划，详细程度：{degree_instruction.get(degree)}。文本内容：{text}\n"
            f"请只返回纯JSON数据，不要使用任何Markdown或代码块格式。"
        )

        # 系统角色中的规则改进
        system_content = (
            "你是一个擅长生成学习计划的助手。\n"
            "请确保生成的学习计划符合以下要求：\n"
            "- 计划格式为 JSON 数组，每个元素包含 \"day\"、\"content\" 以及 \"title\" 字段。\n"
            "- \"day\" 为整数，表示第几天。\n"
            "- \"content\" 为数组，包含每天的具体计划项，每个条目是一个字符串，描述当天的学习任务。\n"
            "- \"title\" 为数组，包含每天的计划概要，每个条目是对应 \"content\" 数组中每个条目的简洁总结。\n"
            "- \"title\" 数组的长度应该与 \"content\" 数组的长度一致，且每个 \"title\" 对应于 \"content\" 中的同一条目。\n"
            "- 遵循用户在提示词中提供的详细程度（degree）要求。\n"
            "- 只返回符合上述格式的 JSON 数据，不要添加额外的解释或文字。"
        )

        payload = {
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_prompt}
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
                plan_text = data['choices'][0]['message']['content'].strip()

                # 尝试解析LLM返回的JSON数据
                try:
                    plan = json.loads(plan_text)
                    # 验证计划的结构
                    if isinstance(plan, list):
                        for day_plan in plan:
                            if not isinstance(day_plan, dict) or 'day' not in day_plan or 'content' not in day_plan:
                                raise ValueError("计划的结构不符合要求")
                            if not isinstance(day_plan['content'], list):
                                raise ValueError("每一天的内容必须是一个数组")
                    else:
                        raise ValueError("计划必须是一个数组")
                except json.JSONDecodeError:
                    return JsonResponse({"code": 1, "msg": f"生成的计划不是有效的JSON格式"}, status=500)
                except ValueError as ve:
                    return JsonResponse({"code": 1, "msg": f"生成的计划结构有误: {str(ve)}"}, status=500)

                return JsonResponse({
                    "code": 0,
                    "msg": "success",
                    "plan": plan
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

@csrf_exempt
def ai_generate(request):
    if request.method == 'POST':
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"}, status=401)

        # 获取前端请求数据
        prompt = request.POST.get('prompt', '').strip()
        AI_model = request.POST.get('AI_model', None)
        length = request.POST.get('length',None)
        tone = request.POST.get('tone', 'neutral')  # 'formal', 'informal', 'humorous', etc.
        style = request.POST.get('style', 'default')  # 'academic', 'creative', etc.
        
        if length:
            try:
                length = int(length)
                if length <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({"code": 1, "msg": "length必须是正整数"}, status=400)
        else:
            length = 300  # 默认长度

        length = min(length, 2000)

        # 验证必填字段
        if not prompt:
            return JsonResponse({"code": 1, "msg": "提示词不能为空"}, status=400)

        if AI_model is None:
            return JsonResponse({"code": 1, "msg": "请选择AI模型"}, status=400)

        # 转换并验证 AI_model
        try:
            AI_model = int(AI_model)
            if AI_model not in [0, 1]:
                raise ValueError
        except ValueError:
            return JsonResponse({"code": 1, "msg": "请选择正确的AI模型"}, status=400)


        # 配置语调和风格
        tone_mapping = {
            'neutral': '',
            'formal': '请使用正式的语气。',
            'informal': '请使用非正式的语气。',
            'humorous': '请使用幽默的语气。',
            'motivational': '请使用激励人心的语气。',
            'serious': '请使用严肃的语气。',
            'friendly': '请使用友好的语气。',
            'sarcastic': '请使用讽刺的语气。',
            'pessimistic': '请使用悲观的语气。'
        }

        style_mapping = {
            'default': '',
            'academic': '请采用学术写作风格。',
            'creative': '请采用创意写作风格。',
            'technical': '请采用技术性的写作风格。',
            'narrative': '请采用叙事性的写作风格。',
            'descriptive': '请采用描述性的写作风格。',
            'concise': '请采用简洁的写作风格。',
            'emotional': '请采用情感丰富的写作风格。'
        }

        tone_instruction = tone_mapping.get(tone, '')
        style_instruction = style_mapping.get(style, '')

        # 配置API请求
        model = "gpt-4o-mini" if AI_model == 0 else "moonshot-v1-8k"
        api_url = "https://api.gptsapi.net/v1/chat/completions" if AI_model == 0 else "https://api.moonshot.cn/v1/chat/completions" 

        # 构建提示词
        prompt_instructions = f"{tone_instruction} {style_instruction} 请生成以下提示词的段落，控制在{length}字：\n\n{prompt}".strip()
        payload = {
            "messages": [
                {"role": "system", "content": "你是一个擅长写作的助手。"},
                {"role": "user", "content": prompt_instructions}
            ],
            "model": model,
            "max_tokens": length + 100
        }
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY if AI_model == 0 else settings.KIMI_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                generated_paragraph = data['choices'][0]['message']['content'].strip()
                return JsonResponse({
                    "code": 0,
                    "msg": "success",
                    "paragraph": generated_paragraph
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
def ai_continue(request):
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
            return JsonResponse({"code": 1, "msg": "需要续写的文本内容不能为空"}, status=400)

        
        if length:
            try:
                length = int(length)
                if length <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({"code": 1, "msg": "length必须是正整数"}, status=400)
        else:
            length = 300  # 默认摘要长度

        length = min(length, 2000)
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
        
        prompt = f"请根据以下文本续写内容，保持语言风格和表述尽可能与原文相同，续写只输出新的内容，输出不要超过{length}字：\n\n{text}"
        payload = {
            "messages": [
                {"role": "system", "content": "你是一个擅长续写文本的助手，能够保持原文的语言风格和表达方式。"},
                {"role": "user", "content": prompt}
            ],
            "model": model,
            "max_tokens": length + 100
        }
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY if AI_model == 0 else settings.KIMI_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                continuation = data['choices'][0]['message']['content'].strip()
                return JsonResponse({
                    "code": 0,
                    "msg": "success",
                    "continuation": continuation
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
def ai_inspiration(request):
    if request.method == 'POST':
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"}, status=401)

        # 获取前端请求数据
        prompt = request.POST.get('prompt', '').strip()
        length = request.POST.get('length', None)
        content_type = request.POST.get('content_type', 'inspiration').strip().lower()
        AI_model = request.POST.get('AI_model', None)

        if not prompt:
            return JsonResponse({"code": 1, "msg": "写作要求或提示词不能为空"}, status=400)

        # 处理并验证长度参数
        if length:
            try:
                length = int(length)
                if length <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({"code": 1, "msg": "length必须是正整数"}, status=400)
        else:
            length = 300  # 默认长度

        length = min(length, 2000)  # 限制最大长度为2000

        # 转换并验证 AI_model
        if AI_model is None:
            return JsonResponse({"code": 1, "msg": "请选择AI模型"}, status=400)
        
        try:
            AI_model = int(AI_model)
            if AI_model not in [0, 1]:
                raise ValueError
        except ValueError:
            return JsonResponse({"code": 1, "msg": "请选择正确的AI模型"}, status=400)

        # 验证并处理 content_type
        valid_types = {
            'inspiration': "写作灵感",
            'outline': "有条理的写作大纲",
            'title': "标题",
            'character_bio': "角色设定",
            'scene_description': "场景描述",
            'dialogue': "对话内容",
            'plot_twist': "情节转折",
            'setting': "环境设定",
            'synopsis': "故事摘要",
            # 可根据需要添加更多类型
        }

        if content_type not in valid_types:
            return JsonResponse({"code": 1, "msg": f"无效的类型。可选类型: {', '.join(valid_types.keys())}"}, status=400)

        # 定义哪些类型只生成一个项目
        single_item_types = {'title', 'character_bio', 'scene_description', 'dialogue', 'plot_twist', 'setting', 'synopsis'}

        # 配置API请求
        model = "gpt-4o-mini" if AI_model == 0 else "moonshot-v1-8k"
        api_url = "https://api.gptsapi.net/v1/chat/completions" if AI_model == 0 else "https://api.moonshot.cn/v1/chat/completions" 
        
        # 构建提示信息和系统消息
        if content_type in single_item_types:
            prompt_instruction = (
                f"请为以下文本内容生成{valid_types[content_type]}。"
                f"只输出一个{valid_types[content_type]}，不要包含任何其他内容。"
                f"输出内容不要超过{length}字。\n\n文本内容：\n\n{prompt}"
            )
            system_content = f"你是一个能够生成{valid_types[content_type]}的助手。请确保只输出一个{valid_types[content_type]}，不要输出多个点，不包含任何其他内容。"
        else:
            prompt_instruction = (
                f"为以下文本内容生成{valid_types[content_type]}，"
                f"输出内容不要超过{length}字。\n\n文本内容：\n\n{prompt}"
            )
            system_content = f"你是一个能够生成{valid_types[content_type]}的助手。"

        payload = {
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt_instruction}
            ],
            "model": model,
            "max_tokens": length + 100  # 估算token数，确保满足长度要求
        }

        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY if AI_model == 0 else settings.KIMI_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                content = data['choices'][0]['message']['content'].strip()
                
                return JsonResponse({
                    "code": 0,
                    "msg": "success",
                    content_type: content
                })
            else:
                return JsonResponse(
                    {"code": 1, "msg": f"调用失败，状态码：{response.status_code}", "details": response.text},
                    status=response.status_code
                )
        except requests.RequestException as e:
            return JsonResponse({"code": 1, "msg": f"请求异常：{str(e)}"}, status=500)

    return JsonResponse({"code": 1, "msg": "无效的请求方法"}, status=405)

import re
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests

@csrf_exempt
def ai_analysis(request):
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
        analysis_type = request.POST.get('type', 'analysis').strip().lower()
        AI_model = request.POST.get('AI_model', None)

        if not text:
            return JsonResponse({"code": 1, "msg": "需要续写的文本内容不能为空"}, status=400)

        # 处理并验证长度参数
        if length:
            try:
                length = int(length)
                if length <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({"code": 1, "msg": "length必须是正整数"}, status=400)
        else:
            length = 300  # 默认长度

        length = min(length, 2000)  # 限制最大长度为2000

        # 转换并验证 AI_model
        if AI_model is None:
            return JsonResponse({"code": 1, "msg": "请选择AI模型"}, status=400)
        
        try:
            AI_model = int(AI_model)
            if AI_model not in [0, 1]:
                raise ValueError
        except ValueError:
            return JsonResponse({"code": 1, "msg": "请选择正确的AI模型"}, status=400)

        # 定义有效的分析类型及其描述
        valid_types = {
            'analysis': "分析",
            'evaluation': "评价",
            'correction': "纠错并指出错误",
            # 可根据需要添加更多类型
        }

        #验证并处理 analysis_type 参数
        if analysis_type not in valid_types:
            return JsonResponse({"code": 1, "msg": f"无效的类型。可选类型: {', '.join(valid_types.keys())}"}, status=400)
        
        # 配置API请求
        model = "gpt-4o-mini" if AI_model == 0 else "moonshot-v1-8k"
        api_url = "https://api.gptsapi.net/v1/chat/completions" if AI_model == 0 else "https://api.moonshot.cn/v1/chat/completions" 
        
        # 构建提示信息和系统消息
        prompt_instruction = (
            f"请为以下文本内容进行{valid_types[analysis_type]}。"
            f"输出内容不要超过{length}字。\n\n文本内容：\n\n{text}"
        )
        system_content = f"你是一个能够进行{valid_types[analysis_type]}的助手。"

        payload = {
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt_instruction}
            ],
            "model": model,
            "max_tokens": length + 100  # 估算token数，确保满足长度要求
        }

        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY if AI_model == 0 else settings.KIMI_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                content = data['choices'][0]['message']['content'].strip()
                
                return JsonResponse({
                    "code": 0,
                    "msg": "success",
                    analysis_type: content
                })
            else:
                return JsonResponse(
                    {"code": 1, "msg": f"调用失败，状态码：{response.status_code}", "details": response.text},
                    status=response.status_code
                )
        except requests.RequestException as e:
            return JsonResponse({"code": 1, "msg": f"请求异常：{str(e)}"}, status=500)

    return JsonResponse({"code": 1, "msg": "无效的请求方法"}, status=405)


