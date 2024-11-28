<template>
  <div class="note-file-container">
    <!-- 左侧文件夹列表 -->
    <div class="sidebar">

      <h2>
        <i class="iconfont icon-wenjianjia" style="font-size: 28px; margin-right: 4px;color: cadetblue;"></i>
        文件夹列表</h2>
      <!-- <button @click="createFolder" class="create-folder-button">新建文件夹</button>    -->
      <button @click="openCreateFolderModal" class="create-folder-button">新建文件夹</button>   
      <button @click="manageFolder" 
      :class="{'manage-folder-button': isManaging, 'create-folder-button': !isManaging}">
        {{ isManaging ? '确定' : '管理文件夹' }}</button>   
      <div class="folder-list">
        <div
          v-for="folder in folders"
          :key="folder.id"
          :class="{'folder-item1': isManaging, 'folder-item': !isManaging}"
          @click="selectFolder(folder.id, folder.name)"
        >
        <h3>{{ folder.name }}</h3>
        <div v-show="isManaging" class="note-actions">
            <i class="rename-button iconfont icon-bianji" @click.stop="renameFolder(folder)"></i>
            <i class="delete-button iconfont icon-shanchu" @click.stop="deleteFolder(folder)"></i>
        </div>
        </div>
      </div>
    </div>

    <!-- 右侧笔记展示区 -->
    <div class="content">
      <Note v-if="selectedFolderId !== null" :folderId="selectedFolderId" :folderName="selectedFolderName" />
    </div>
    <!-- 新建文件夹弹窗 -->
    <div v-if="isModalVisible" class="modal-overlay" @click="closeCreateFolderModal">
      <div class="modal" @click.stop>
        <h3>新建文件夹</h3>
        <input v-model="newFolderName" type="text" class="modal-input" placeholder="请输入文件夹名称"  @keydown="handleKeydown" />
        <div class="modal-actions">
          <button @click="createFolder" class="modal-button">创建</button>
          <button @click="closeCreateFolderModal" class="modal-button cancel">取消</button>
        </div>
      </div>
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
const isModalVisible = ref(false);  // 控制弹窗的显示
const newFolderName = ref('');  // 用于新建文件夹名称的输入框

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

// 打开新建文件夹弹窗
const openCreateFolderModal = () => {
  isModalVisible.value = true;
};

// 关闭新建文件夹弹窗
const closeCreateFolderModal = () => {
  isModalVisible.value = false;
  newFolderName.value = '';  // 清空输入框
};

// 新建文件夹
const createFolder = async () => {
  if (newFolderName.value) {
    try {
      const response = await request.post(`/ez-note/folder/create`, { name: newFolderName.value });
      if (response.code === 0) {
        folders.value.push(response.data);
        closeCreateFolderModal();  // 关闭弹窗
      } else {
        alert(response.msg);
      }
    } catch (error) {
      console.error('创建文件夹失败:', error);
      alert('创建文件夹失败，请稍后重试');
    }
  } else {
    alert('请输入文件夹名称');
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

// 处理按回车新建文件夹
const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    createFolder();
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
  padding-top: 0px;
  background: #fff;
  border-right: 1px solid #ddd;
  /* box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1); */
  display: flex;
  flex-direction: column;
}
.create-folder-button {
  background-color: #00a687;
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
  background-color:#009691;
}

.folder-item:hover {
  background-color: #e7e7e7;
  transform: scale(1.05);
}

.manage-folder-button{
  background-color: #c7184a;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-bottom: 10px;
  text-align: center;
}

.manage-folder-button:hover{
  background-color:#b7003f;
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

.folder-item1 {
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


.folder-item h3 {
  margin:auto;
  margin-left: 10px;
  font-size: 16px;
  color: #333;
}

.folder-item1 h3 {
  margin:auto;
  margin-left: 10px;
  font-size: 16px;
  color: #333;
}

.content {
  flex-grow: 1;
  padding: 20px;
  background: #fff;
  /* box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1); */
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

  .sidebar h2 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

  .content {
    margin-top: 20px;
  }
}

/* 按钮样式 */
.view-button {
  width: 40px;
  height: 30px;
  border: none;
  font-size: 30px;
  /* background-color: transparent; */
  cursor: pointer;
  transition: color 0.3s ease, transform 0.3s ease;
}

.rename-button {
  font-size: 28px;
  margin-right: 10px;
  color:#009691;
  cursor: pointer;
}

.rename-button:hover{
  color:#429490;
  transform: scale(1.1);
  transition: all .3s ease;
}

.delete-button {
  font-size: 28px;
  color: #dc3545;
  cursor: pointer;
}

.delete-button:hover{
  color: #b7003f;
  transform: scale(1.1);
  transition: all .3s ease;
}

.note-actions {
  display: flex;
  justify-content:end;
  margin: auto 5px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  width: 300px;
}

.modal h3 {
  text-align: center;
  margin-top: 5px;
  margin-bottom: 20px;
  font-size: 18px;
  color: #333;
}

.modal-input {
  width: 90%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  outline: none;
}

.modal-actions {
  width: 55%;
  display: flex;
  margin: auto;
  justify-content: space-between;
}

.modal-button {
  width: 70px;
  padding: 8px 15px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.modal-button.cancel {
  background-color: #f44336;
  color: white;
}

.modal-button.cancel:hover {
  background-color: #e53935;
}

.modal-button {
  background-color: #429490;;
  color: white;
}

.modal-button:hover {
  background-color: #009691;
}

.note-actions {
  display: flex;
}
</style>
