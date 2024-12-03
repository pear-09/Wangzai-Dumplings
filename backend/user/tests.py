from django.test import TestCase
from user.models import User
from django.urls import reverse

class UserAuthTestCase(TestCase):
    def setUp(self):
        # 设置注册和登录视图的 URL
        self.register_url = reverse('register')  # 假设注册视图的名称是 register
        self.login_url = reverse('login')        # 假设登录视图的名称是 login

        # 预设的用户数据
        self.user_data = {
            "username": "testuser",
            "password": "securepassword123"
        }

    def test_register_success(self):
        # 测试注册成功
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, self.user_data['username'])

    def test_register_failure_empty_fields(self):
        # 测试注册失败（用户名或密码为空）
        response = self.client.post(self.register_url, data={"username": "", "password": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 1)
        self.assertIn("用户名和密码不能为空", response.json()['msg'])

    def test_login_success(self):
        # 先创建用户以便登录
        User.objects.create_user(**self.user_data)

        # 测试登录成功
        response = self.client.post(self.login_url, data=self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 0)
        self.assertIn("token", response.json())  # 验证返回包含 token

    def test_login_failure_wrong_credentials(self):
        # 先创建用户
        User.objects.create_user(**self.user_data)

        # 测试登录失败（密码错误）
        response = self.client.post(self.login_url, data={
            "username": self.user_data['username'],
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 1)
        self.assertIn("用户名或密码错误", response.json()['msg'])

    def test_login_failure_user_not_exist(self):
        # 测试登录失败（用户不存在）
        response = self.client.post(self.login_url, data={
            "username": "nonexistentuser",
            "password": "somepassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 1)
        self.assertIn("用户名或密码错误", response.json()['msg'])
