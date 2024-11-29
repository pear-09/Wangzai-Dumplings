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

const isRenameModalVisible = ref(false);  // 控制重命名文件夹弹窗的显示
const isDeleteModalVisible = ref(false);  // 控制删除文件夹弹窗的显示
const renameFolderName = ref('');  // 用于重命名文件夹的输入框
const folderToRename = ref<Notefiles | null>(null);  // 用于存储需要重命名的文件夹
const folderToDelete = ref<Notefiles | null>(null);  // 用于存储需要删除的文件夹

// 获取文件夹列表
const getFolders = async () => {
  try {
    const response = await request.get(`/ez-note/folder/get-all`);  // 使用 request 实例
    console.log(response);  // 打印整个响应对象
    if (response.code === 0) {
      folders.value = response.data;
      console.log(folders.value);
       // 默认选择第一个文件夹
       if (folders.value.length > 0) {
        selectedFolderId.value = folders.value[0].id;
        selectedFolderName.value = folders.value[0].name;
      }
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

// 打开重命名文件夹弹窗
const openRenameFolderModal = (folder: Notefiles) => {
  folderToRename.value = folder;
  renameFolderName.value = folder.name;
  isRenameModalVisible.value = true;
};

// 关闭重命名文件夹弹窗
const closeRenameFolderModal = () => {
  isRenameModalVisible.value = false;
  renameFolderName.value = '';  // 清空输入框
};

// 重命名文件夹
const renameFolder = async () => {
  if (folderToRename.value && renameFolderName.value !== folderToRename.value.name) {
    try {
      const response = await request.put(`/ez-note/folder/rename`, { id: folderToRename.value.id, name: renameFolderName.value });
      if (response.code === 0) {
        folderToRename.value.name = renameFolderName.value;
        closeRenameFolderModal();  // 关闭弹窗
      } else {
        alert(response.msg);
      }
    } catch (error) {
      console.error('重命名文件夹失败:', error);
      alert('重命名失败，请稍后重试');
    }
  }
};

// 打开删除文件夹弹窗
const openDeleteFolderModal = (folder: Notefiles) => {
  folderToDelete.value = folder;
  isDeleteModalVisible.value = true;
};

// 关闭删除文件夹弹窗
const closeDeleteFolderModal = () => {
  isDeleteModalVisible.value = false;
};

// 删除文件夹
const deleteFolder = async () => {
  if (folderToDelete.value) {
    try {
      const formData = new FormData();
      formData.append('folder_id', String(folderToDelete.value.id)); // 确保 ID 转换为字符串

      const response = await request.post(`/ez-note/folder/delete`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      if (response.code === 0) {
        folders.value = folders.value.filter(f => f.id !== folderToDelete.value?.id);
        closeDeleteFolderModal();  // 关闭弹窗
      } else {
        alert(response.msg);
      }
    } catch (error) {
      console.error('删除文件夹失败:', error);
      alert('删除失败，请稍后重试');
    }
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
            <i class="rename-button iconfont icon-bianji" @click.stop="openRenameFolderModal(folder)"></i>
            <i class="delete-button iconfont icon-shanchu" @click.stop="openDeleteFolderModal(folder)"></i>
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
        <h2>新建文件夹</h2>
        <i class="iconfont icon-cuocha_kuai" @click="closeCreateFolderModal"></i>
        <input v-model="newFolderName" type="text" class="modal-input" placeholder="请输入文件夹名称"  @keydown="handleKeydown" />
        <div class="modal-actions">
          <button @click="createFolder" class="modal-button">创建</button>
          <button @click="closeCreateFolderModal" class="modal-button cancel">取消</button>
        </div>
      </div>
    </div>
  </div>
  <!-- 重命名文件夹弹窗 -->
  <div v-if="isRenameModalVisible" class="modal-overlay" @click="closeRenameFolderModal">
      <div class="modal" @click.stop>
        <h2>重命名文件夹</h2>
        <i class="iconfont icon-cuocha_kuai" @click="closeRenameFolderModal"></i>
        <input v-model="renameFolderName" type="text" class="modal-input" placeholder="请输入新的文件夹名称" />
        <div class="modal-actions">
          <button @click="renameFolder" class="modal-button">确认</button>
          <button @click="closeRenameFolderModal" class="modal-button cancel">取消</button>
        </div>
      </div>
    </div>

    <!-- 删除文件夹弹窗 -->
    <div v-if="isDeleteModalVisible" class="modal-overlay" @click="closeDeleteFolderModal">
      <div class="modal" @click.stop>
        <h2>确认删除 "{{ folderToDelete?.name }}"</h2>
        <i class="iconfont icon-cuocha_kuai" @click="closeDeleteFolderModal"></i>
        <i class="iconfont icon-cuowukongxin" style="font-size: 100px; color: #b7003f; "></i>
        <div class="modal-actions">
          <button @click="deleteFolder" class="modal-button">确认</button>
          <button @click="closeDeleteFolderModal" class="modal-button cancel">取消</button>
        </div>
      </div>
    </div>
</template>

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
/* 遮罩层 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);  /* 背景模糊效果，调整模糊程度 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  display: flex;
  flex-direction: column;
  position: relative;
  width: 380px;
  /* height: 300px; */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  background-color: rgba(255, 255, 255, 0.9);  /* 弹窗背景颜色及透明度 */
}

.modal .icon-cuocha_kuai{
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 20px
}

.modal .icon-cuocha_kuai:hover{
  color: #b7003f;
}

.modal .icon-cuowukongxin{
  text-align: center;
  transform: translateY(-20px);
}

.modal h2 {
  text-align: center;
  margin-top: 10px;
  margin-bottom: 40px;
  /* font-size: 20px; */
  color: #333333c9;
}

.modal-input {
  width: 90%;
  padding: 10px;
  margin-bottom: 40px;
  border: none;
  border-bottom: 1px solid #009691;
  background-color: transparent;
  outline: none;
}

.modal-actions {
  width: 50%;
  display: flex;
  margin: auto;
  justify-content: space-between;
}

.modal-button {
  width: 80px;
  height: 40px;
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
  background-color: #429490;
  color: white;
}

.modal-button:hover {
  background-color: #009691;
}

.note-actions {
  display: flex;
}
</style>
