<template>
  <div class="write-container">
    <!-- 左侧侧边栏 -->
    <div :class="['sidebar', { collapsed: isCollapsed }]">
      <div class="sidebar-header">
        <span>文件夹</span>
        <button class="toggle-button" @click="toggleSidebar">
          {{ isCollapsed ? '>' : '<' }}
        </button>
      </div>
      <ul class="folder-list">
        <!-- 只显示默认文件夹 -->
        <li v-if="defaultFolder" :key="defaultFolder.id" class="folder-item">
          <div class="folder-header">
            <span
              class="folder-toggle"
              @click="toggleFolder(defaultFolder.id)"
            >
              {{ expandedFolders.includes(defaultFolder.id) ? '|' : '>' }}
            </span>
            <span class="folder-name">{{ defaultFolder.name }}</span>
            <button
              class="add-doc-button"
              @click.stop="createDocument(defaultFolder.id)"
            >
              +
            </button>
          </div>
          <!-- 文档列表 -->
          <ul
            v-if="expandedFolders.includes(defaultFolder.id)"
            class="document-list"
          >
            <li
              v-for="doc in documents"
              :key="doc.id"
              class="document-item"
              @click="editDocument(doc.id)"
            >
              {{ doc.title }}
            </li>
          </ul>
        </li>
        <!-- 如果没有加载完数据，显示加载中 -->
        <li v-else>
          <p>加载中...</p>
        </li>
      </ul>
    </div>

    <!-- 右侧内容区域 -->
    <div class="content-area">
      <h2 v-if="defaultFolder">当前文件夹: {{ defaultFolder.name }}</h2>
      <p v-else>请选择一个文件夹以显示文档</p>
      <router-view></router-view> <!-- 动态加载右侧内容 -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import request from '@/utils/request'; // 引入 request.ts 中的 axios 实例
import { useRouter } from 'vue-router';

// 状态变量
const defaultFolder = ref(null); // 存储默认文件夹
const documents = ref([]); // 存储文档列表
const expandedFolders = ref<number[]>([]); // 存储展开的文件夹 ID
const isCollapsed = ref(false);
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
        // 如果没有找到“写作助手”文件夹，创建它
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

// 切换文件夹的展开/收起状态
const toggleFolder = (folderId: number) => {
  const index = expandedFolders.value.indexOf(folderId);
  if (index > -1) {
    expandedFolders.value.splice(index, 1);
  } else {
    expandedFolders.value.push(folderId);
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


// 切换侧边栏收起状态
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
};

// 初始化
onMounted(fetchDefaultFolderAndDocuments);
</script>


<style scoped>
.write-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 20%;
  background-color: #f7f7f7;
  transition: width 0.3s ease;
}

.sidebar.collapsed {
  width: 5%;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.add-doc-button,
.toggle-button {
  border: none;
  background-color: #5c6bc0;
  color: #fff;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  text-align: center;
  line-height: 24px;
  cursor: pointer;
}

.folder-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.folder-item {
  padding: 10px;
}

.folder-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.folder-toggle {
  cursor: pointer;
  margin-right: 10px;
}

.folder-name {
  cursor: pointer;
  flex-grow: 1;
}

.document-list {
  list-style: none;
  padding: 0 10px;
  margin: 0;
}

.document-item {
  cursor: pointer;
  padding: 5px 0;
}

.content-area {
  flex-grow: 1;
  padding: 20px;
}
</style>
