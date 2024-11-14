<template>
    <div class="schedule">
      <h1>当天任务</h1>
      <div v-if="loading">加载中...</div>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="tasks.length">
        <ul>
          <li v-for="task in tasks" :key="task.id">
            <div class="task">
              <h3>{{ task.title }}</h3>
              <p>{{ task.description }}</p>
              <span>时间: {{ task.time }}</span>
              <span>状态: {{ task.status }}</span>
            </div>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>没有任务</p>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import axios from 'axios';
  import type { GetTasksResponse, Task } from '@/types/api/getTasks'; // 导入接口类型
  
  export default defineComponent({
    name: 'Schedule',
    setup() {
      // 状态管理
      const tasks = ref<Task[]>([]);  // 存储任务列表
      const loading = ref<boolean>(true);  // 加载状态
      const error = ref<string>('');  // 错误信息
  
      // 获取任务数据的函数
      const fetchTasks = async () => {
        try {
            const apiUrl = import.meta.env.VITE_API_URL;            // 从环境变量获取 API 地址
  
          const response = await axios.get<GetTasksResponse>(`${apiUrl}/ez-note/date/get`);
  
          // 如果请求成功，更新任务数据
          if (response.data.code === 0) {
            tasks.value = response.data.data;  // 获取任务列表并更新
          } else {
            error.value = '获取任务失败: ' + response.data.msg;  // 错误信息处理
          }
        } catch (err) {
          error.value = '加载任务时发生错误: ' + err;  // 错误信息处理
        } finally {
          loading.value = false;  // 无论成功与否，都将加载状态设置为 false
        }
      };
  
      // 在组件加载时调用获取任务数据的函数
      onMounted(() => {
        fetchTasks();
      });
  
      return {
        tasks,
        loading,
        error
      };
    }
  });
  </script>
  
  <style scoped>
  .schedule {
    padding: 20px;
  }
  
  .task {
    border: 1px solid #ccc;
    padding: 10px;
    margin: 10px 0;
  }
  
  .task h3 {
    margin: 0;
  }
  
  .task p {
    margin: 5px 0;
  }
  
  .error {
    color: red;
    font-weight: bold;
  }
  </style>
  
