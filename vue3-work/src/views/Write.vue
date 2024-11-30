<template>
  <!-- 整个页面的容器 -->
  <div class="page-container">
    <!-- 写作助手的主内容区域 -->
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
          <div v-if="isManaging" class="manage-actions">
            <button @click.stop="confirmDelete(doc.id)">删除</button>
            <button @click.stop="openRenameModal(doc.id)">重命名</button>
          </div>
        </li>
      </ul>

      <!-- 如果没有文档 -->
      <p v-else class="empty-text">此文件夹没有文档，请点击新建文档。</p>

      <!-- 重命名弹窗 -->
      <div v-if="newTitleModalOpen" class="rename-modal">
        <input v-model="newTitle" placeholder="输入新的文件名" />
        
        <!-- 新增的按钮容器，用于并排显示确认和取消按钮 -->
        <div class="rename-modal-buttons">
          <button class="confirm" @click="renameDocument(deletingNoteId, newTitle)">确认</button>
          <button class="cancel" @click="closeRenameModal">取消</button>
        </div>
      </div>
    </div>

    <!-- AI功能区域 -->
    <div class="ai-features-wrapper">
      <h3 class="ai-title">AI帮你做</h3>
      <div class="ai-features-container">
        <div class="ai-feature" @click="navigateToEdit('段落美化')">
          <img src="@/assets/writeAI1.png" alt="段落美化" class="ai-icon" />
          <span class="ai-text">段落美化</span>
        </div>
        <div class="ai-feature" @click="navigateToEdit('生成段落')">
          <img src="@/assets/writeAI2.png" alt="生成段落" class="ai-icon" />
          <span class="ai-text">生成段落</span>
        </div>
        <div class="ai-feature" @click="navigateToEdit('续写内容')">
          <img src="@/assets/writeAI3.png" alt="续写内容" class="ai-icon" />
          <span class="ai-text">续写内容</span>
        </div>
        <div class="ai-feature" @click="navigateToEdit('写作提示')">
          <img src="@/assets/writeAI4.png" alt="写作提示" class="ai-icon" />
          <span class="ai-text">写作提示</span>
        </div>
        <div class="ai-feature" @click="navigateToEdit('文章分析')">
          <img src="@/assets/writeAI5.png" alt="文章分析" class="ai-icon" />
          <span class="ai-text">文章分析</span>
        </div>
      </div>
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

const navigateToEdit = (featureType: string) => {
  // 假设 defaultFolder.value.id 是您想要的 folderId
  if (defaultFolder.value) {
    createDocument(defaultFolder.value.id);
  } else {
    console.error('默认文件夹未定义');
  }
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
      closeRenameModal(); // 成功后关闭弹窗
      await fetchDocumentsInDefaultFolder(defaultFolder.value.id); // 刷新文档列表
    } else {
      alert(response.msg);
    }
  } catch (error) {
    console.error('重命名文档失败:', error);
  }
};

// 初始化
onMounted(() => {
  fetchDefaultFolderAndDocuments();
});
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
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.manage-doc-button:hover {
  background-color: #fb8c00;
  transform: translateY(-2px); /* 鼠标悬浮时按钮上升 */
}

.manage-doc-button:active {
  background-color: #f57c00;
  transform: translateY(0); /* 按钮点击时恢复位置 */
}

/* 管理文档按钮的整体布局 */
.manage-actions {
  display: flex;
  gap: 1px; /* 增加按钮之间的间距 */
  align-items: center;
  justify-content: flex-end; /* 将按钮靠右对齐 */
  margin-left: auto; /* 让按钮区域自动推到最右侧 */
}

.manage-actions button {
  padding: 6px 12px;
  margin-right: 1px;
  background-color: #ff5722; /* 删除按钮 */
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
}

/* 删除按钮悬浮效果 */
.manage-actions button:hover {
  background-color: #e64a19;
  transform: translateY(-2px); /* 鼠标悬浮时按钮上升 */
}

/* 删除按钮点击效果 */
.manage-actions button:active {
  background-color: #d84315;
  transform: translateY(0); /* 按钮点击时恢复位置 */
}

/* 重命名按钮样式 */
.manage-actions button:nth-child(2) {
  background-color: #4caf50; /* 绿色按钮 */
}

/* 重命名按钮悬浮效果 */
.manage-actions button:nth-child(2):hover {
  background-color: #45a049;
  transform: translateY(-2px);
}

/* 重命名弹窗样式 */
.rename-modal {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.rename-modal input {
  padding: 8px 16px;
  font-size: 16px;
  margin-bottom: 10px;
  width: 250px;
  border-radius: 6px;
  border: 1px solid #ccc;
  transition: border 0.3s ease;
}

.rename-modal input:focus {
  border-color: #4caf50;
  outline: none;
}

.rename-modal button {
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.rename-modal button:hover {
  background-color: #45a049;
}

.rename-modal button:active {
  background-color: #388e3c;
}

/* 确认和取消按钮容器使用 Flexbox 横向排列 */
.rename-modal-buttons {
  display: flex; 
  gap: 15px; /* 按钮间距 */
  justify-content: center; /* 居中对齐 */
  width: 100%; /* 确保按钮容器占满宽度 */
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

/* 调整文档列表的布局 */
.document-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap; /* 允许换行 */
  gap: 10px; /* 设置文档之间的间隔 */
}

/* 为每个文档项添加边框和调整大小 */
.document-item {
  padding: 10px; /* 减少内边距 */
  cursor: pointer;
  font-size: 16px; /* 减小字体大小 */
  border: 1px solid #e0e0e0; /* 添加边框 */
  border-radius: 4px; /* 圆角边框 */
  transition: background-color 0.3s ease;
  flex: 1 1 calc(33.333% - 20px); /* 设置每个文档项的宽度和伸缩性 */
  max-width: calc(33.333% - 20px); /* 设置最大宽度 */
  margin: 5px; /* 调整文档项的外边距 */
  box-sizing: border-box; /* 确保边框和内边距包含在宽度内 */
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  flex-wrap: nowrap; /* 不允许换行 */
  /* 添加阴影效果 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* 阴影的颜色、模糊程度等 */
  transition: box-shadow 0.3s ease, transform 0.3s ease; /* 为了更好的过渡效果 */
}

/* 确保文档项在较小屏幕上也能良好显示 */
@media (max-width: 768px) {
  .document-item {
    flex: 1 1 100%; /* 在小屏幕上，每个文档项占满整行 */
    max-width: 100%;
  }
}

.document-item:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* 增加更大的阴影 */
  transform: translateY(-4px); /* 鼠标悬停时让文档框稍微上浮 */
}

.document-item:active {
  background-color: #f0f0f0;
}

/* 文档标题：确保文字不会换行 */
.document-item .doc-title {
  flex-grow: 1; /* 使文档名称占据剩余的空间 */
  white-space: nowrap; /* 禁止换行 */
  overflow: hidden;
  text-overflow: ellipsis; /* 超过宽度时显示省略号 */
}

.ai-features-wrapper {
  width: 360px; /* 固定宽度 */
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 简单阴影 */
  border-radius: 8px; /* 圆角效果 */
}

.ai-title {
  text-align: center;
  margin-bottom: 20px;
  font-weight: bold;
  font-size: 23px; /* 调整字体大小 */
}

.ai-features-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 20px; /* 保留padding，但给容器添加背景色 */
  background-color: #fff; /* 添加背景色 */
}

.ai-feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  background-color: #ffffff; /* 浅灰色背景 */
  border: 1px solid #ccc; /* 边框 */
  border-radius: 8px; /* 圆角边框 */
  cursor: pointer;
  text-align: center;
}

.ai-icon {
  width: 55px; /* 图标大小 */
  height: 55px; /* 图标大小 */
  margin-bottom: 10px;
}

.ai-text {
  font-size: 16px;
  color: #333;
}

/* 页面整体按钮的风格和布局 */
.page-container {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}

</style>



