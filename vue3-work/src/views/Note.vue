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
const isModalVisible = ref(false); // 控制弹窗显示
const newNoteTitle = ref(''); // 新建笔记的默认标题
const isDeleteModalVisible = ref(false); // 控制删除确认弹窗显示
const deletingNoteId = ref<string | null>(null); // 待删除笔记的 ID
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

// 显示新建笔记弹窗
const showNewNoteModal = () => {
  isModalVisible.value = true;
};

// 处理弹窗确认逻辑
const confirmNewNote = () => {
  isModalVisible.value = false;
  console.log(newNoteTitle.value);
  router.push({ name: 'noteDetail', params: { folder_id: props.folderId, id: 'new', title: newNoteTitle.value } });
};

// 关闭弹窗
const closeModal = () => {
  isModalVisible.value = false;
};

// 显示删除确认弹窗
const showDeleteModal = (noteId: string) => {
  deletingNoteId.value = noteId;
  isDeleteModalVisible.value = true;
};

// 确认删除笔记
const confirmDeleteNote = async () => {
  if (!deletingNoteId.value) return;
  try {
    const formData = new FormData();
    formData.append("note_id", deletingNoteId.value);

    const response = await request.post(`/ez-note/note/delete`, formData);

    if (response.code === 0) {
      const noteIndex = currentFolder.value.notes.findIndex(note => note.id.toString() === deletingNoteId.value);
      if (noteIndex !== -1) {
        currentFolder.value.notes.splice(noteIndex, 1);
      }
      alert("笔记删除成功");
    } else {
      alert(response.msg);
    }
  } catch (error) {
    console.error("删除笔记失败:", error);
    alert("请求失败，请稍后重试");
  } finally {
    closeDeleteModal();
  }
};
// 关闭删除确认弹窗
const closeDeleteModal = () => {
  isDeleteModalVisible.value = false;
  deletingNoteId.value = null;
};
// 处理按回车新建笔记
const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    confirmNewNote();
  }
};
</script>

<template>
  <div class="note-list-container">
    <h1 class="page-title">{{ currentFolder?.name || '我的笔记' }}</h1>
    <div class="action-buttons">
      <button class="view-button" >导入文件</button>
      <button class="view-button" @click="showNewNoteModal">新建笔记</button>
      <button class="view-button manage-button"
       @click="toggleManaging">
        {{ isManaging ? '确定' : '管理笔记' }}
      </button>
    </div>

    <div v-if="currentFolder && currentFolder.notes.length > 0" class="note-list">
      <div v-for="note in currentFolder.notes" :key="note.id" class="note-item"
        @click="goToNoteDetail(note.id.toString(), note.folder_id.toString())"
        :class="{'note-item gl': isManaging, 'note-item bgl': !isManaging}">
        <div class="note-header">
          <h2 class="note-title">{{ note.title }}</h2>
          <p>{{ note.created_at }}</p>
        </div>
        <div v-show="isManaging" class="note-actions">
            <i class="rename-button iconfont icon-bianji"></i>
            <i class="delete-button iconfont icon-shanchu" @click.stop="showDeleteModal(note.id.toString())"></i>
        </div>
      </div>
    </div>
    <div v-else>
      <p style="font-weight: 700;">暂时没有笔记，赶快去创建一个吧！</p>
    </div>
  </div>

  <!-- 新建笔记弹窗 -->
  <div v-if="isModalVisible" class="modal">
    <div class="modal-content">
      <h2>新建笔记</h2>
      <input v-model="newNoteTitle" type="text" placeholder="请输入笔记标题" class="modal-input" @keydown="handleKeydown"/>
      <div class="modal-actions">
        <button @click="confirmNewNote" class="modal-button confirm-button">确定</button>
        <button @click="closeModal" class="modal-button cancel-button">取消</button>
      </div>
    </div>
  </div>

   <!-- 删除确认弹窗 -->
   <div v-if="isDeleteModalVisible" class="modal">
      <div class="modal-content">
        <h3>确认删除</h3>
        <p>确定要删除这篇笔记吗？</p>
        <div class="modal-actions">
          <button @click="confirmDeleteNote" class="modal-button confirm-button">删除</button>
          <button @click="closeDeleteModal" class="modal-button cancel-button">取消</button>
        </div>
      </div>
    </div>
</template>

<style scoped>
.modal {
  z-index: 2;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.3s ease;
}
.modal h3{
  text-align: center;
  margin-top: 0px;
}
.modal-content {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  width: 350px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
}

.modal-input {
  width: 90%;
  padding: 12px;
  margin: 10px 0;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s ease;
}

.modal-input:focus {
  border-color: #759a8b;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.modal-button {
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  border: none;
}

.confirm-button {
  background-color: #429490;
  color: #fff;
}

.confirm-button:hover {
  background-color: #009691;;
  /* transform: translateY(-2px); */
}

.cancel-button {
  background-color: #dc3545;
  color: #fff;
}

.cancel-button:hover {
  background-color: #c82333;
  /* transform: translateY(-2px); */
}

/* 页面布局 */
.note-list-container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Roboto', sans-serif;
  /* background-color: #f9f9f9; */
  border-radius: 8px;
  /* box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1); */
  border: none;
}

/* 页面标题 */
.page-title {
  font-size: 2.2rem;
  font-weight: bold;
  margin-top: 0px;
  margin-bottom: 20px;
  color: #333;
  text-transform: uppercase;
}

/* 按钮组 */
.action-buttons {
  display: flex;
  justify-content: baseline;
  gap: 15px;
  margin-bottom: 20px;
}

/* 按钮样式 */
.view-button {
  background-color: #00a687;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.view-button:hover {
  background-color: #009691;
  /* transform: translateY(-2px); */
}

.manage-button {
  background-color: #c7184a;
}

.manage-button:hover {
  background-color: #b7003f;
}

.note-actions{
  display: flex;
  align-items: center;
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

.bgl:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

/* 笔记标题 */
.note-header {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.note-title {
  font-size: 1.35rem;
  font-weight: bold;
  color: #333;
  margin: 0;
  line-height: 1.4;
}

.note-header p{
  margin-top: 5px;
  margin-bottom: 0px;
  color: #888;
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

  .note-list {
    grid-template-columns: 1fr;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

@keyframes slideUp {
  0% { transform: translateY(30px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}
</style>

