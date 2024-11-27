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
      
      // 刷新页面并跳转到首页
      window.location.reload();  // 刷新页面
      router.push('/home');  // 跳转到首页
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

// 跳转到注册页面
const goToRegister = () => {
  router.push('/register');
};
</script>

<template>
  <div class="home-container">
    <div class="illustration">
      <img src="../assets/undraw_open_note_cgre.svg" alt="illustration" />
    </div>
    <div class="content">
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

        <!-- 注册链接 -->
        <div class="register-link">
          <p>没有账号？ <a href="#" @click.prevent="goToRegister">去注册</a></p>
        </div>
      </div>
    </div>
    <!-- 装饰图案 -->
    <img class="leaf1" src="../assets/green.svg" alt="leaf decoration" />
    <img class="leaf2" src="../assets/green.svg" alt="leaf decoration" />
  </div>
</template>

<style scoped>
.home-container {
  padding: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #f0f2f5, #d1e0e0), url('../assets/background.svg');
  background-size: cover;
  background-position: center;
  position: relative;
}

.illustration {
  position: absolute;
  left: 8%;
  top: 50%;
  transform: translateY(-50%);
}

.illustration img {
  width: 600px; /* 控制插画大小 */
  height: auto;
}

.content {
  margin-left: 488px; /* 右移登录框，使其不覆盖插画 */
  width: 100%;
  max-width: 400px;
}

.welcome-message, .login-message {
  background-color: rgba(255, 255, 255, 0.8); /* 半透明背景 */
  color: #333;
  padding: 30px 50px;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  text-align: center;
  margin: 20px;
  position: relative;
}

.welcome-message {
  background-color: #4CAF50;
}

.login-message {
  background-color: #ffffff;
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
  text-align: left;
}

label {
  display: block;
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
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

.register-link {
  margin-top: 20px;
}

.register-link a {
  color: #4CAF50;
  font-weight: bold;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

/* 装饰图案 */
.leaf1, .leaf2 {
  position: absolute;
  top: 30px;
  z-index: 1;
  opacity: 0.6;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
}

.leaf1 {
  left: 10%;
  width: 180px;
  height: 180px;
  animation: floatLeaf1 6s infinite;
}

.leaf2 {
  right: 10%;
  width: 200px;
  height: 200px;
  animation: floatLeaf2 8s infinite;
}

/* 动画效果 */
@keyframes floatLeaf1 {
  0% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-20px) rotate(15deg);
  }
  50% {
    transform: translateY(0) rotate(0deg);
  }
  75% {
    transform: translateY(20px) rotate(-15deg);
  }
  100% {
    transform: translateY(0) rotate(0deg);
  }
}

@keyframes floatLeaf2 {
  0% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-30px) rotate(-10deg);
  }
  50% {
    transform: translateY(0) rotate(0deg);
  }
  75% {
    transform: translateY(30px) rotate(10deg);
  }
  100% {
    transform: translateY(0) rotate(0deg);
  }
}

@media (max-width: 768px) {
  .home-container {
    padding: 15px;
  }

  .illustration {
    display: none; /* 移动端不显示插画 */
  }

  .content {
    margin-left: 0;
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

  .leaf1, .leaf2 {
    width: 150px;
    height: 150px;
  }
}
</style>
