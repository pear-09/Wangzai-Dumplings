<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import request from '@/utils/request';  // 引入 request 实例
import { useRouter } from 'vue-router';
import type { Note, GetNotesResponse, Notelist } from '@/types/api/getNotelist';

// 路由实例
const router = useRouter();

// 接收父组件传递的 folderId 和 folderName props
const props = defineProps<{
  folderId: number;
  folderName: string;
}>();

// 当前文件夹的数据，使用 GetNotesResponse 中的 Note[] 数组
const currentFolder = ref<{
  id: number;
  name: string;
  notes: Notelist[]; // 默认应该是空数组
}>({
  id: 0, // 默认 ID
  name: '', // 默认名称
  notes: [] // 默认是空数组
});

// 管理模式状态
const isManaging = ref(false);

// 获取该文件夹下的笔记
const getNotes = async (folderId: number) => {
  try {
    const response = await request.get<GetNotesResponse>(`/ez-note/note/query-all`, {
      params: { folder_id: folderId }
    });

    if (response.code === 0) {
      const notesData = response.data || []; // 确保后端返回的数据是数组
      currentFolder.value = { id: folderId, name: props.folderName, notes: notesData }; // 使用 props.folderName
    } else {
      alert(response.data.msg);
    }
  } catch (error) {
    console.error('获取笔记失败:', error);
    alert('请求失败，请稍后重试');
  }
};

// 根据文件夹 ID 获取相应的文件夹信息
onMounted(() => {
  if (props.folderId) {
    getNotes(props.folderId);  // 传递有效的 folderId
  }
});

// 监听 folderId 的变化，并重新获取笔记
watch(() => props.folderId, (newFolderId) => {
  if (newFolderId) {
    getNotes(newFolderId);  // 传递新的 folderId 进行获取笔记
  }
});

// 切换管理模式
const toggleManaging = () => {
  isManaging.value = !isManaging.value;
};

const goToNoteDetail = (id: string) => {
  router.push({ name: 'noteDetail', params: { folder_id: props.folderId, id } });
};

const goToNewNote = () => {
  router.push({ name: 'noteDetail', params: { folder_id: props.folderId, id: 'new' } });
};

//删除笔记
const deleteNote = async (event: Event, noteId: string) => {
  // 阻止事件冒泡，防止点击删除按钮时触发跳转
  event.stopPropagation();

  // 确认删除操作
  if (confirm("确定要删除这篇笔记吗？")) {
    try {
      // 使用 FormData 构造请求体
      const formData = new FormData();
      formData.append("note_id", noteId);

      // 发起 POST 请求，拦截器会自动设置 Content-Type
      const response = await request.post(`/ez-note/note/delete`, formData);

      if (response.code === 0) {
        // 删除成功后，更新笔记列表
        const noteIndex = currentFolder.value.notes.findIndex(note => note.id.toString() === noteId);
        if (noteIndex !== -1) {
          currentFolder.value.notes.splice(noteIndex, 1); // 从本地删除该笔记
        }
        alert("笔记删除成功");
      } else {
        alert(response.msg); // 如果删除失败，显示错误信息
      }
    } catch (error) {
      console.error("删除笔记失败:", error);
      alert("请求失败，请稍后重试");
    }
  }
};
</script>

<template>
  <div class="note-list-container">
    <h1 class="page-title">{{ currentFolder?.name || '我的笔记' }}</h1>
    <div class="action-buttons">
      <button class="view-button" @click="goToNewNote">新建笔记</button>
      <button class="view-button manage-button" @click="toggleManaging">
        {{ isManaging ? '确定' : '管理笔记' }}
      </button>
    </div>
    
    <div v-if="currentFolder && currentFolder.notes.length > 0" class="note-list">
      <div v-for="note in currentFolder.notes" :key="note.id" class="note-item" @click="goToNoteDetail(note.id.toString(), note.folder_id.toString())">
        <div class="note-header">
          <h2 class="note-title">{{ note.title }}</h2>
        </div>
        <div v-show="isManaging" class="note-actions">
          <button class="view-button delete-button" @click="deleteNote($event, note.id.toString())">删除</button>
        </div>
      </div>
    </div>
    <div v-else>
      <p>该文件夹下没有笔记</p>
    </div>
  </div>
</template>



<style scoped>
/* 页面布局 */
.note-list-container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Roboto', sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

/* 页面标题 */
.page-title {
  /* text-align: center; */
  font-size: 2.2rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
  text-transform: uppercase;
  /* transform: translateX(-380px); */
}

/* 按钮组 */
.action-buttons {
  display: flex;
  justify-content:baseline;
  gap: 15px;
  margin-bottom: 20px;
  /* transform: translateX(-350px); */
}

/* 按钮样式 */
.view-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.view-button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.manage-button {
  background-color: #28a745;
}

.manage-button:hover {
  background-color: #218838;
}

.delete-button {
  background-color: #dc3545;
}

.delete-button:hover {
  background-color: #c82333;
}

/* 笔记列表 */
.note-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

/* 单个笔记项 */
.note-item {
  display: flex;
  justify-content: space-between;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.note-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

/* 笔记标题 */
.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.note-title {
  font-size: 1.35rem;
  font-weight: bold;
  color: #333;
  margin: 0;
  line-height: 1.4;
}

.note-date {
  font-size: 0.9rem;
  color: #888;
}

/* 笔记内容 */
.note-content {
  font-size: 1rem;
  color: #555;
  margin-top: 10px;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .note-list-container {
    width: 100%;
    padding: 15px;
  }

  .note-title {
    font-size: 1.15rem;
  }

  .note-content {
    font-size: 0.95rem;
  }

  .view-button {
    padding: 8px 15px;
    font-size: 0.9rem;
  }

  .note-list {
    grid-template-columns: 1fr; /* 单列布局 */
  }
}

</style>

