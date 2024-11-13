<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router'; // 引入 useRoute 和 useRouter

// 获取路由参数（笔记的id）
const route = useRoute();
const router = useRouter();

// 获取笔记ID，检查是否为新建笔记
const noteId = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id;
const isNewNote = noteId === 'new';  // 如果 noteId 是 'new'，表示新建笔记

// 模拟的笔记数据（后端实际接口会根据ID返回笔记信息）
const notes = [
  { id: '1', title: '学习 Vue.js', content: '今天学习了 Vue 3 的基本语法和响应式系统。', date: '2024-11-01' },
  { id: '2', title: '工作项目计划', content: '与团队成员讨论了项目的进度和下一步计划。', date: '2024-11-02' },
  { id: '3', title: '阅读《深入浅出React》', content: '阅读了书中的“React生命周期”章节，理解了 React 的渲染机制。', date: '2024-11-03' },
  { id: '4', title: '锻炼计划', content: '跑步和做瑜伽，保持身体健康。', date: '2024-11-04' }
];

// 当前笔记
const note = ref<{ id: string, title: string, content: string, date: string }>({
  id: '',
  title: '',
  content: '',
  date: ''
});

// 编辑模式
const isEditing = ref(false);

// 拉取笔记内容（用于编辑）
const fetchNote = async (id: string) => {
  const fetchedNote = notes.find(n => n.id === id);
  if (fetchedNote) {
    note.value = { ...fetchedNote }; // 更新当前笔记内容
  }
};

// 初始化新建笔记
const initNewNote = () => {
  note.value = {
    id: '',
    title: '',
    content: '',
    date: new Date().toISOString().slice(0, 10)  // 设置当前日期
  };
};

// 进入编辑模式
const startEditing = () => {
  isEditing.value = true;
};

// 保存笔记
const saveNote = () => {
  if (isNewNote) {
    // 新建笔记，生成一个新的ID并添加到列表
    const newId = (notes.length + 1).toString(); // 假设新ID是现有数据长度 + 1
    notes.push({ ...note.value, id: newId });
  } else {
    // 编辑已存在的笔记
    const index = notes.findIndex(n => n.id === note.value.id);
    if (index !== -1) {
      notes[index] = { ...note.value };
    }
  }

  // 保存完成后返回到笔记列表
  router.push({ name: 'biji' });

  
};

// 取消编辑，恢复原始数据
const cancelEdit = () => {
  if (isNewNote) {
    // 如果是新建笔记，直接返回列表
    router.push({ name: 'biji' });
  } else {
    fetchNote(noteId);  // 取消时重新拉取原始数据
  }
};

// 页面加载时获取笔记数据或初始化新建笔记
onMounted(() => {
  if (isNewNote) {
    initNewNote();
  } else {
    fetchNote(noteId);
  }
});
</script>

<template>
  <div class="note-detail-container">
    <h1 class="note-title">{{ isNewNote ? '新建笔记' : note.title }}</h1>
    <p class="note-date">{{ note.date }}</p>

    <!-- 编辑模式下显示输入框 -->
    <div class="note-content">
      <template v-if="isEditing">
        <input v-model="note.title" class="note-title-input" placeholder="请输入笔记标题" required />
        <textarea v-model="note.content" class="note-textarea" placeholder="编辑笔记内容" required></textarea>
      </template>
      <template v-else>
        <!-- <h3>{{ note.title }}</h3> -->
        <p>{{ note.content }}</p>
      </template>
    </div>

    <div class="note-actions">
      <button v-if="isEditing" @click="saveNote" class="view-button">保存</button>
      <button v-if="isEditing" @click="cancelEdit" class="view-button">取消</button>
      <button v-else @click="startEditing" class="view-button">编辑</button>
    </div>
  </div>
</template>

<style scoped>
.note-detail-container {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.note-title {
  font-size: 2rem;
  font-weight: bold;
}

.note-date {
  font-size: 1rem;
  color: #888;
}

.note-content {
  margin-top: 20px;
  font-size: 1.25rem;
  line-height: 1.6;
}

.note-textarea {
  width: 100%;
  height: 200px;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
}

.note-actions {
  margin-top: 20px;
}

.view-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 4px;
  margin-right: 10px;
}

.view-button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
