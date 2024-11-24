<template>
  <div class="note-file-container">
    <div class="content">
      <h2>我的文档</h2>
      
      <!-- 管理文档按钮 -->
      <div class="actions">
        <button @click="createFolder">新建文档</button>
        <button @click="manageFolder">{{ isManaging ? '确定' : '管理文档' }}</button>
      </div>

      <!-- 文档列表 -->
      <div class="folder-list">
        <div v-for="folder in folders" :key="folder.id" class="folder-item">
          <h3 @click="editDocument(folder.id)">{{ folder.name }}</h3> <!-- 点击标题进入编辑页面 -->
          <div v-show="isManaging" class="note-actions">
            <button @click.stop="renameFolder(folder)">编辑标题</button>
            <button @click.stop="deleteFolder(folder)">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import request from '@/utils/request';  // 引入 request.ts 中的 axios 实例
import { useRouter } from 'vue-router';

import type { Notefiles } from '@/types/api/getNotefiles';

const router = useRouter();
const folders = ref<Notefiles[]>([]);
const isManaging = ref(false);

// 获取文档列表
const getFolders = async () => {
  try {
    const response = await request.get('/ez-note/folder/get-all');
    if (response.code === 0) {
      folders.value = response.data;
    } else {
      alert(response.msg);
    }
  } catch (error) {
    console.error('获取文档列表失败:', error);
    alert('请求失败，请稍后重试');
  }
};

// 点击进入编辑页面
const editDocument = (folderId: number) => {
  router.push({ name: 'writeEdit', params: { id: folderId } });
};

// 新建文件夹
const createFolder = async () => {
  const newFolderName = prompt('请输入文件夹名称');
  if (newFolderName) {
    try {
      const response = await request.post('/ez-note/folder/create', { name: newFolderName });
      if (response.code === 0) {
        folders.value.push(response.data);
      } else {
        alert(response.msg);
      }
    } catch (error) {
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
    request.put('/ez-note/folder/rename', { id: folder.id, name: newName })
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
    request.post('/ez-note/folder/delete', { folder_id: folder.id })
      .then(response => {
        if (response.code === 0) {
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
  getFolders();  // 获取文档列表
});
</script>

<style scoped>
.note-file-container {
  padding: 20px;
}
.content {
  max-width: 800px;
  margin: 0 auto;
}
h2 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}
.actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.folder-list {
  margin-top: 20px;
}
.folder-item {
  background: #f7f7f7;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
}
.folder-item h3 {
  margin: 0;
  cursor: pointer;
}
.note-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #5C6BC0;
  color: white;
}
button:hover {
  background-color: #3949AB;
}
</style>
