// src/utils/request.ts
import axios from 'axios';
import type { AxiosInstance} from 'axios';



const request: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 100000, // 请求超时时间，单位毫秒
});

// 请求拦截器：可以在这里添加认证 token 等信息
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token'); // 添加 token
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    // 检查请求数据类型
    if (config.data instanceof FormData) {
      // 如果是 FormData，删除 Content-Type，交给浏览器自动设置
      delete config.headers['Content-Type'];
    } else {
      // 确保其他请求未强制修改 Content-Type，保留 Axios 默认行为
      config.headers['Content-Type'] = config.headers['Content-Type'] || 'application/json';
    }

    return config;
  },
  (error) => Promise.reject(error)
);


// 响应拦截器：可以处理全局的响应错误
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('请求失败：', error);
    return Promise.reject(error);
  }
);



export default request;
