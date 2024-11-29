<template>
  <div class="content-area">
    <!-- 文件夹信息显示 -->
    <h2 v-if="defaultFolder" class="folder-title">{{ defaultFolder.name }}</h2>
    <p v-else class="loading-text">加载中...</p>

    <!-- 管理文档按钮，点击后启用删除和重命名功能 -->
    <div v-if="defaultFolder" class="manage-doc-button-container">
      <button class="manage-doc-button" @click="toggleManaging">
        {{ isManaging ? '取消管理' : '管理文档' }}
      </button>
    </div>

    <!-- 新建文档按钮 -->
    <div v-if="defaultFolder" class="create-doc-button-container">
      <button class="create-doc-button" @click="createDocument(defaultFolder.id)">
        新建文档
      </button>
    </div>

    <!-- 显示文档列表 -->
    <ul v-if="documents.length > 0" class="document-list">
      <li
        v-for="doc in documents"
        :key="doc.id"
        class="document-item"
        @click="editDocument(doc.id)"
      >
        {{ doc.title }}
        <!-- 管理模式下，显示删除和重命名按钮 -->
        <button v-if="isManaging" @click.stop="confirmDelete(doc.id)">删除</button>
        <button v-if="isManaging" @click.stop="openRenameModal(doc.id)">重命名</button>
      </li>
    </ul>

    <!-- 如果没有文档 -->
    <p v-else class="empty-text">此文件夹没有文档，请点击新建文档。</p>

    <!-- 重命名弹窗 -->
    <div v-if="newTitleModalOpen" class="rename-modal">
      <input v-model="newTitle" placeholder="输入新的文件名" />
      <button @click="renameDocument(deletingNoteId, newTitle)">确认</button>
      <button @click="closeRenameModal">取消</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import request from '@/utils/request'; 
import { useRouter } from 'vue-router';

// 状态变量
const defaultFolder = ref(null); // 存储默认文件夹
const documents = ref([]); // 存储文档列表
const isManaging = ref(false); // 控制是否进入管理状态
const deletingNoteId = ref(null); // 存储当前删除文档的 ID
const newTitle = ref(''); // 存储重命名时的新文件名
const newTitleModalOpen = ref(false); // 控制重命名弹窗
const router = useRouter();

// 获取默认文件夹及其文档
const fetchDefaultFolderAndDocuments = async () => {
  try {
    const folderResponse = await request.get('/ez-note/folder/get-all');
    if (folderResponse.code === 0) {
      const folder = folderResponse.data.find(f => f.name === '写作助手');
      if (folder) {
        defaultFolder.value = folder;
        await fetchDocumentsInDefaultFolder(folder.id); // 获取该文件夹下的文档
      } else {
        const createResponse = await request.post('/ez-note/folder/create', {
          name: '写作助手',
        });
        if (createResponse.code === 0) {
          defaultFolder.value = createResponse.data;
          await fetchDocumentsInDefaultFolder(createResponse.data.id); // 获取新创建文件夹的文档
        }
      }
    }
  } catch (error) {
    console.error('获取默认文件夹失败:', error);
  }
};

// 获取文档列表
const fetchDocumentsInDefaultFolder = async (folderId: number) => {
  try {
    const response = await request.get('/ez-note/note/query-all', {
      params: { folder_id: folderId },
    });
    if (response.code === 0) {
      documents.value = response.data;
    } else {
      alert(response.msg);
    }
  } catch (error) {
    console.error('获取文档失败:', error);
  }
};

// 创建新文档，跳转到编辑页面
const createDocument = (folderId: number) => {
  const defaultDocName = '无标题';
  router.push({
    name: 'writeEdit',
    query: {
      folder_id: folderId,
      docName: defaultDocName,
      isNew: 1, // 新建文档标识
    },
  });
};

// 编辑文档
const editDocument = (docId: number) => {
  router.push({
    name: 'writeEdit',
    params: { id: docId }, // 使用路由参数传递文档 ID
    query: {
      isNew: 0, // 编辑已有文档标识
    },
  });
};

// 切换管理模式
const toggleManaging = () => {
  isManaging.value = !isManaging.value;
};

// 删除文档
const confirmDelete = (noteId: number) => {
  const confirmDelete = window.confirm('确认删除此文档吗？');
  if (confirmDelete) {
    deleteDocument(noteId);
  }
};

// 删除文档
const deleteDocument = async (noteId: number) => {
  try {
    const formData = new FormData();
    formData.append('note_id', String(noteId)); // 使用 FormData 传递 note_id
    const response = await request.post('/ez-note/note/delete', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // 指定 Content-Type 为 form-data
      },
    });
    if (response.code === 0) {
      await fetchDocumentsInDefaultFolder(defaultFolder.value.id); // 删除成功后刷新文档列表
    } else {
      alert(response.msg);
    }
  } catch (error) {
    console.error('删除文档失败:', error);
  }
};

// 打开重命名弹窗
const openRenameModal = (noteId: number) => {
  newTitleModalOpen.value = true;
  deletingNoteId.value = noteId;
};

// 关闭重命名弹窗
const closeRenameModal = () => {
  newTitleModalOpen.value = false;
  newTitle.value = ''; // 清空文件名输入
};

// 重命名文档
const renameDocument = async (noteId: number, newTitle: string) => {
  try {
    const formData = new FormData();
    formData.append('note_id', String(noteId)); // 使用 FormData 传递 note_id
    formData.append('title', newTitle); // 使用 FormData 传递新标题
    const response = await request.post('/ez-note/note/update/title', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // 指定 Content-Type 为 form-data
      },
    });
    if (response.code === 0) {
      await fetchDocumentsInDefaultFolder(defaultFolder.value.id); // 重命名成功后刷新文档列表
      closeRenameModal(); // 关闭弹窗
    } else {
      alert(response.msg);
    }
  } catch (error) {
    console.error('重命名文档失败:', error);
  }
};

onMounted(fetchDefaultFolderAndDocuments);
</script>



<style scoped>
/* 新增管理按钮样式 */
.manage-doc-button-container {
  margin: 20px 0;
  text-align: right;
}

.manage-doc-button {
  padding: 8px 16px;
  background-color: #ff9800; /* 橙色按钮 */
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.manage-doc-button:hover {
  background-color: #fb8c00;
}

.manage-actions {
  display: inline-block;
  margin-left: 10px;
}

.manage-actions button {
  padding: 4px 8px;
  margin-right: 5px;
  background-color: #ff5722; /* 删除按钮 */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.manage-actions button:hover {
  background-color: #e64a19;
}

/* 重命名弹窗 */
.rename-popup {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.rename-popup input {
  padding: 5px 10px;
  font-size: 16px;
  margin-bottom: 10px;
  width: 200px;
}

.rename-popup button {
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.rename-popup button:hover {
  background-color: #45a049;
}
/* 确保页面内容左对齐，背景色简约 */
.content-area {
  width: 70%; /* 宽度占 70% */
  padding: 20px;
  background-color: #fff; /* 背景色 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 简单阴影 */
  border-radius: 8px; /* 圆角效果 */
  overflow: hidden;
  margin-left: 0; /* 去除居中，紧贴左边 */
}

.folder-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.loading-text, .empty-text {
  font-size: 16px;
  color: #999;
  text-align: center;
}

.create-doc-button-container {
  margin: 20px 0;
  text-align: right;
}

.create-doc-button {
  padding: 8px 16px;
  background-color: #4caf50; /* 绿色按钮 */
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.create-doc-button:hover {
  background-color: #45a049;
}

.document-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.document-item {
  padding: 12px;
  cursor: pointer;
  font-size: 18px;
  border-bottom: 1px solid #e0e0e0;
  transition: background-color 0.3s ease;
}

.document-item:hover {
  background-color: #f5f5f5;
}

.document-item:active {
  background-color: #f0f0f0;
}
</style>



