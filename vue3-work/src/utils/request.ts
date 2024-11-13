
// src/utils/request.ts
import axios from "axios";

const request = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 10000, // 请求超时时间，单位毫秒
})

// 请求拦截器：可以在这里添加认证 token 等信息
request.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('auth_token');  // 如果有 token，可以添加到请求头中
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
  
  // 响应拦截器：可以处理全局的响应错误
  request.interceptors.response.use(
    (response) => response.data,
    (error) => {
      // 处理错误，例如弹出错误提示
      console.error('请求失败：', error);
      return Promise.reject(error);
    }
  );
  


export default request