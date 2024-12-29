from django.test import TestCase
from rest_framework.test import APIClient
from user.models import User
from note.models import Tag, Note
from user.utils import generate_jwt_token  # 导入生成 Token 的函数


class CreateNoteViewTests(TestCase):

    def setUp(self):
        # 初始化测试数据
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        # 使用生成函数创建 JWT Token
        self.token = generate_jwt_token(self.user)
        # 配置 API 客户端
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')  # 设置认证头

        self.url = '/ez-note/note/create'

    def test_create_note_success(self):
        # 测试成功创建笔记
        payload = {
            "title": "Test Note",
            "content": "This is a test note.",
            "folder_id": "1",  # folder_id 应传递为字符串形式
            "tags": ["Tag1", "Tag2"]  # tags 也需要传递为列表
        }

        # 设置 form-data 格式，使用 data 参数
        response = self.client.post(self.url, data=payload)

        # 验证响应状态
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)

        # 验证数据库中的记录
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Tag.objects.count(), 2)

    def test_create_note_without_title(self):
        # 测试未提供标题时默认使用 "新建笔记"
        payload = {
            "content": "Content without title",
            "folder_id": 11,
            "tags": []
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["title"], '新建笔记')

    def test_create_note_missing_folder(self):
        # 测试未提供 folder_id 的情况
        payload = {
            "title": "Note without folder",
            "content": "Content without folder",
            "tags": []
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(response.json()['msg'], "所属文件夹不能为空")

    def test_create_note_invalid_token(self):
        # 测试无效 Token 的情况
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        payload = {
            "title": "Test Note",
            "content": "This is a test note.",
            "folder_id": "1",
            "tags": ["Tag1"]
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 1)
        self.assertTrue("Token 验证失败" in response.json()['msg'])
