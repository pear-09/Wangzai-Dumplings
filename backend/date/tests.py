from django.test import TestCase
from django.urls import reverse
from user.models import User
from datetime import datetime, timedelta
from rest_framework.test import APIClient
import json
from user.utils import generate_jwt_token

class DatePlanTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        # 使用生成函数创建 JWT Token
        self.token = generate_jwt_token(self.user)
        # 设置 URL 路径
        self.generate_url = '/ez-note/date/generate'
        self.create_url = reverse('create')

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # 设置认证头


    def test_create_success(self):
        # 测试成功创建日程
        payload = {
            "title": "Test Meeting",
            "description": "Description of the test meeting.",
            "time": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S')  # 明天的时间
        }

        response = self.client.post(self.create_url,data=json.dumps(payload),content_type='application/json')

        # 验证响应
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['msg'], "日程创建成功")
        self.assertIn("date_id", response.json()['data'])

    def test_generate_success(self):
        # 测试成功生成日程
        payload = {
            "startday": (datetime.now()).strftime('%Y-%m-%d'),  # 当前日期作为起始日期
            "plan": [
                {
                    "day": 1,
                    "content": ["Content for day 1"],
                    "title": ["Meeting 1"]
                },
                {
                    "day": 2,
                    "content": ["Content for day 2"],
                    "title": ["Meeting 2"]
                }
            ]
        }

        response = self.client.post(self.generate_url, data=json.dumps(payload),
                                    content_type='application/json')
        print(response.json())

        # 验证响应
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['msg'], "日程生成并存储成功")
        self.assertIn("data", response.json())
        self.assertEqual(len(response.json()['data']), 2)  # 应该生成两个日程

    def test_create_failure_invalid_json(self):
        # 测试发送无效 JSON 数据
        invalid_payload = '{"title": "Test Meeting", "description": "Description}'

        response = self.client.post(self.create_url, data=invalid_payload
                                        ,content_type='application/json')
        print(response.json())

        # 验证响应
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['code'], 1)
        self.assertIn("无效的 JSON 数据", response.json()['msg'])

    def test_generate_failure_invalid_json(self):
        # 测试发送无效 JSON 数据
        invalid_payload = '{"startday": "2024-12-01", "plan": [{"day": 1, "content": "test_content"}]}'

        response = self.client.post(self.generate_url, data=invalid_payload, content_type='application/json')
        print(response.json())

        # 验证响应
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 1)