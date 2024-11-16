<template>
  <div class="note-file-container">
    <!-- 左侧文件夹列表 -->
    <div class="sidebar">
      <h2>文件夹列表</h2>
      <button @click="createFolder" class="create-folder-button">新建文件夹</button>   
      <button @click="manageFolder" class="create-folder-button">{{ isManaging ? '确定' : '管理文件夹' }}</button>   
      <div class="folder-list">
        <div
          v-for="folder in folders"
          :key="folder.id"
          class="folder-item"
          @click="selectFolder(folder.id, folder.name)"
        >
        <h3>{{ folder.name }}</h3>
        <div v-show="isManaging" class="note-actions">
            <button class="view-button rename-button" @click.stop="renameFolder(folder)">编辑</button>
            <button class="view-button delete-button" @click.stop="deleteFolder(folder)">删除</button>
          </div>

        </div>
      </div>
    </div>

    <!-- 右侧笔记展示区 -->
    <div class="content">
      <Note v-if="selectedFolderId !== null" :folderId="selectedFolderId" :folderName="selectedFolderName" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import request from '@/utils/request';  // 引入 request.ts 中的 axios 实例
import Note from './Note.vue';  // 导入 Note 子组件

import type { Notefiles } from '@/types/api/getNotefiles';


const folders = ref<Notefiles[]>([]);
const selectedFolderId = ref<number | null>(null);
const selectedFolderName = ref<string>(''); // 添加一个 ref 用于保存文件夹的名字
const isManaging = ref(false);

// 获取文件夹列表
const getFolders = async () => {
  try {
    const response = await request.get(`/ez-note/folder/get-all`);  // 使用 request 实例
    console.log(response);  // 打印整个响应对象
    if (response.code === 0) {
      folders.value = response.data;
      console.log(folders.value);
      
    } else {
      alert(response.msg);
    }
  } catch (error) {
    console.error('获取文件夹列表失败:', error);
    alert('请求失败，请稍后重试');
  }
};

// 选择文件夹
const selectFolder = (folderId: number, folderName: string) => {
  selectedFolderId.value = folderId;
  selectedFolderName.value = folderName;

  // 保证切换文件夹不会影响 isManaging 的状态
  console.log('当前管理模式:', isManaging.value);
};

//新建文件夹
const createFolder = async () => {
  const newFolderName = prompt('请输入文件夹名称');
  if (newFolderName) {
    try {
      // 将新文件夹名称以 folder_name 作为字段名传递
      const response = await request.post(`/ez-note/folder/create`, { name: newFolderName });  // 使用 folder_name
      if (response.code === 0) {
        folders.value.push(response.data);
        console.log("成功创建文件夹")
      } else {
        alert(response.msg);
      }
    } catch (error) {
      console.error('创建文件夹失败:', error);
      alert('创建文件夹失败，请稍后重试');
    }
  }
};

// 切换管理模式
const manageFolder = () => {
  isManaging.value = !isManaging.value;
};

// 重命名文件夹
const renameFolder = (folder: Notefiles) => {
  const newName = prompt('请输入新的文件夹名称', folder.name);
  if (newName && newName !== folder.name) {
    request.put(`/ez-note/folder/rename`, { id: folder.id, name: newName })
      .then(response => {
        if (response.code === 0) {
          folder.name = newName;
        } else {
          alert(response.msg);
        }
      })
      .catch(err => {
        console.error('重命名失败', err);
        alert('重命名失败，请稍后重试');
      });
  }
};

// 删除文件夹
const deleteFolder = (folder: Notefiles) => {
  if (confirm(`确定要删除文件夹 "${folder.name}" 吗？`)) {
    // 创建 FormData
    const formData = new FormData();
    formData.append('folder_id', String(folder.id)); // 确保 ID 转换为字符串

    request
      .post(`/ez-note/folder/delete`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // 设置 Content-Type
        },
      })
      .then(response => {
        if (response.code === 0) {
          // 删除成功后从列表移除文件夹
          folders.value = folders.value.filter(f => f.id !== folder.id);
        } else {
          alert(response.msg);
        }
      })
      .catch(err => {
        console.error('删除失败', err);
        alert('删除失败，请稍后重试');
      });
  }
};


onMounted(() => {
  getFolders();  // 获取文件夹数据
});
</script>

<style scoped>
.note-file-container {
  display: flex;
  font-family: 'Arial', sans-serif;
  min-height: 100vh;
  background: #f5f5f5;
}

.sidebar {
  width: 250px;
  padding: 20px;
  background: #fff;
  border-right: 1px solid #ddd;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.sidebar h2 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.create-folder-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-bottom: 10px;
  text-align: center;
}

.create-folder-button:hover {
  background-color: #45a049;
}

.folder-list {
  display: flex;
  flex-direction: column;
}

.folder-item {
  height: 30px;
  display: flex;
  justify-content: space-between;
  background-color: #fafafa;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.folder-item:hover {
  background-color: #e7e7e7;
  transform: scale(1.05);
}

.folder-item h3 {
  margin:auto;
  margin-left: 10px;
  font-size: 16px;
  color: #333;
}

.content {
  flex-grow: 1;
  padding: 20px;
  background: #fff;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
}

@media (max-width: 768px) {
  .note-file-container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #ddd;
    padding: 10px;
  }

  .content {
    margin-top: 20px;
  }
}

/* 按钮样式 */
.view-button {
  width: 60px;
  height: 25px;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.rename-button {
  background-color: #ffc107;
  margin-right: 5px;
}

.delete-button {
  background-color: #dc3545;
}

.note-actions {
  display: flex;
  justify-content:end;
  margin: auto 5px;
}
</style>
