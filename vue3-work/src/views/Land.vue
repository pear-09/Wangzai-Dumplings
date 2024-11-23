<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';  // 用于页面跳转
import axios from 'axios';  // 用于发送请求

// 登录表单的字段
const username = ref('');
const password = ref('');
const errorMessage = ref('');

// 用于判断用户是否已登录
const isLoggedIn = ref(false);  
const loggedInUsername = ref('');  // 用于存储已登录的用户名

// 用 router 实例进行页面跳转
const router = useRouter();

// 检查 localStorage 中是否有用户名和 token，判断是否登录
onMounted(() => {
  const storedUsername = localStorage.getItem('username');
  const token = localStorage.getItem('auth_token');
  if (storedUsername && token) {
    loggedInUsername.value = storedUsername;
    isLoggedIn.value = true;
  }
});

// 登录请求
interface LoginResponse {
  code: number;
  msg: string;
  token?: string;
}

const handleLogin = async () => {
  errorMessage.value = '';

  // 检查表单是否填写完整
  if (!username.value || !password.value) {
    errorMessage.value = '用户名和密码不能为空';
    return;
  }

  try {
    const response = await axios.post<LoginResponse>(
      `${import.meta.env.VITE_API_URL}/ez-note/user/login`, 
      {
        username: username.value,
        password: password.value
      },
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        }
      }
    );

    if (response.data.code === 0) {
      // 登录成功
      localStorage.setItem('auth_token', response.data.token || '');
      localStorage.setItem('username', username.value);
      loggedInUsername.value = username.value;
      isLoggedIn.value = true;

      alert('登录成功');
      router.push('/home');  // 跳转到主页
    } else {
      errorMessage.value = response.data.msg || '登录失败，请稍后再试';
    }
  } catch (error) {
    errorMessage.value = '登录失败，请稍后再试';
    console.error('登录失败:', error);
  }
};

// 登出请求
const handleLogout = () => {
  localStorage.removeItem('username');
  localStorage.removeItem('auth_token');
  loggedInUsername.value = '';
  isLoggedIn.value = false;
};
</script>

<template>
  <div class="home-container">
    <div v-if="isLoggedIn" class="welcome-message">
      <h2>欢迎回来，{{ loggedInUsername }}！</h2>
      <p>您已成功登录。</p>
      <button @click="handleLogout">登出</button>
    </div>
    <div v-else class="login-message">
      <h2>您尚未登录</h2>
      <p>请先登录以访问完整功能。</p>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名:</label>
          <input
            v-model="username"
            type="text"
            id="username"
            placeholder="请输入用户名"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">密码:</label>
          <input
            v-model="password"
            type="password"
            id="password"
            placeholder="请输入密码"
            required
          />
        </div>
        <button type="submit">登录</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  padding: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #f0f2f5, #d1e0e0);
}

.welcome-message {
  background-color: #4CAF50;
  color: #0a0a0a;
  padding: 30px 50px;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
  margin: 20px;
}

.login-message {
  /* background-color: #FF9800; */
  color: rgb(17, 16, 16);
  padding: 30px 50px;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
  margin: 20px;
}

h2 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 10px;
}

p {
  font-size: 18px;
  margin-top: 15px;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  margin-top: 15px;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #45a049;
  transform: translateY(-2px);
}

button:active {
  transform: translateY(2px);
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

.form-group {
  margin-bottom: 25px;
}

label {
  display: block;
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
  transform: translateX(-180px);
}

input {
  width: 100%;
  padding: 12px;
  margin-top: 5px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: border-color 0.3s ease;
}

input:focus {
  border-color: #4CAF50;
  outline: none;
}

input::placeholder {
  color: #aaa;
}

@media (max-width: 768px) {
  .home-container {
    padding: 15px;
  }

  .welcome-message,
  .login-message {
    padding: 20px;
    max-width: 90%;
  }

  h2 {
    font-size: 24px;
  }

  button {
    font-size: 16px;
  }

  input {
    padding: 10px;
  }
}
</style>
