<template>
  <div class="home-container">
    <div class="illustration">
      <img src="../assets/undraw_well_done_re_3hpo.svg" alt="illustration" />
    </div>
    <div class="content">
      <div class="login-message">
        <h2>注册</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="username">用户名:</label>
            <input v-model="user.username" type="text" id="username" placeholder="请输入用户名" required />
          </div>
          <div class="form-group">
            <label for="password">密码:</label>
            <input v-model="user.password" type="password" id="password" placeholder="请输入密码" required />
          </div>
          <button type="submit">注册</button>
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        </form>
      </div>
    </div>
    <!-- 装饰图案 -->
    <img class="leaf1" src="../assets/green.svg" alt="leaf decoration" />
    <img class="leaf2" src="../assets/green.svg" alt="leaf decoration" />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import axios from 'axios';

const user = reactive({
  username: '',
  password: '',
});

const errorMessage = ref<string>('');

const handleSubmit = async () => {
  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/ez-note/user/register`, user, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    if (response.data.code === 0) {
      alert('注册成功!');
      // 可以添加跳转到登录页面的逻辑，例如：
      // router.push('/login');
    } else {
      errorMessage.value = response.data.msg;
    }
  } catch (error: any) {
    errorMessage.value = error.response?.data?.msg || '注册失败';
  }
};
</script>

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
  top: 45%;
  transform: translateY(-50%);
}

.illustration img {
  width: 488px; /* 控制插画大小 */
  height: auto;
}

.content {
  margin-left: 488px; /* 右移注册框，使其不覆盖插画 */
  width: 100%;
  max-width: 400px;
  margin-top: -20px;
}

.login-message {
  background-color: rgba(255, 255, 255, 0.8); /* 半透明背景 */
  color: #333;
  padding: 30px 50px;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  text-align: center;
  margin: 10px 20px;
  position: relative;
}

h2 {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 10px;
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

button {
  width: 100%;
  padding: 14px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
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
</style>
