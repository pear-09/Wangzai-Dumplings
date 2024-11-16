<template>
  <div class="register-container">
    <h2>注册</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">用户名:</label>
        <input v-model="user.username" type="text" id="username" required />
      </div>
      <div class="form-group">
        <label for="password">密码:</label>
        <input v-model="user.password" type="password" id="password" required />
      </div>
      <button type="submit">注册</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
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
      // 这里可以添加跳转到登录页面的逻辑
    } else {
      errorMessage.value = response.data.msg;
    }
  } catch (error: any) {
    errorMessage.value = error.response?.data?.msg || '注册失败';
  }
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background: linear-gradient(135deg, #f3f4f7, #e0e8e8);
  border-radius: 10px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  font-size: 28px;
  color: #333;
  font-weight: 600;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
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
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
  background-color: #fff;
  transition: border 0.3s ease, box-shadow 0.3s ease;
}

input:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
  outline: none;
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
</style>
