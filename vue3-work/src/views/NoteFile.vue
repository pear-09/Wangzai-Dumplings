<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// 导入接口定义
import type { GetNotefilesResponse, Notefiles } from '@/types/api/getNotefiles';

// 定义存储文件夹数据的 ref
const folders = ref<Notefiles[]>([]);

// 路由
const router = useRouter();

// 获取笔记文件夹列表
const getFolders = async () => {
  try {
    // 调用接口获取文件夹数据
    const response = await axios.get<GetNotefilesResponse>(`${import.meta.env.VITE_API_URL}/ez-note/folder/get-all`);
    console.log(response.data); // 打印返回的数据，确保结构正确

    if (response.data.code === 0) {
      // 请求成功，更新 folders 数据
      folders.value = response.data.data;
    } else {
      // 如果接口返回 code 不是 0，弹出错误信息
      alert(response.data.msg);
    }
  } catch (error) {
    console.error("获取文件夹列表失败:", error);
    alert('请求失败，请稍后重试');
  }
};

// 跳转到文件夹详情页（即笔记列表）
const goToFolderDetail = (id: number) => {
  router.push({ name: 'biji', params: { id } });
};

// 新建文件夹
const createFolder = () => {
  const newFolderName = prompt('请输入文件夹名称');
  if (newFolderName) {
    // 假设 ID 以某种方式生成
    folders.value.push({
      id: folders.value.length + 1,  // 为新文件夹生成 ID（假设为下一个数字）
      user_id: 1,  // 假设用户 ID 为 1
      name: newFolderName,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      deleted_at: null,
    });
  }
};



// 在组件挂载时调用 getFolders 获取文件夹列表
onMounted(() => {
  getFolders();
});
</script>

<template>
  <div class="folder-list-container">
    <h1 class="folder-list-title">文件夹列表</h1>
    <button class="create-folder-button" @click="createFolder">新建文件夹</button>
    
    <div class="folder-list">
      <div v-for="folder in folders" :key="folder.id" class="folder-item" @click="goToFolderDetail(folder.id)">
        <div class="folder-item-header">
          <h2 class="folder-name">{{ folder.name }}</h2>
          <!-- <p class="folder-note-count">包含 {{ folder.notes.length }} 个笔记</p> -->
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 页面布局 */
.folder-list-container {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.folder-list-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
}

/* 文件夹列表 */
.folder-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 20px;
}

/* 单个文件夹项 */
.folder-item {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.folder-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

/* 文件夹名称 */
.folder-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.folder-name {
  font-size: 1.25rem;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.folder-note-count {
  font-size: 0.875rem;
  color: #888;
}

/* 新建文件夹按钮 */
.create-folder-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  margin-bottom: 20px;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.3s;
}

.create-folder-button:hover {
  background-color: #0056b3;
}
</style>


<style scoped>
.folder-list-container {
  padding: 20px;
  background-color: #f4f6f9;
}

.folder-list-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.create-folder-button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 20px;
  transition: background-color 0.3s;
}

.create-folder-button:hover {
  background-color: #45a049;
}

.folder-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.folder-item {
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.folder-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.folder-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.folder-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.folder-note-count {
  font-size: 14px;
  color: #777;
}

@media (max-width: 600px) {
  .folder-list {
    grid-template-columns: 1fr;  /* 手机屏幕单列显示 */
  }

  .create-folder-button {
    width: 100%;
  }
}
</style>
