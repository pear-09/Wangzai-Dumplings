<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import request from '@/utils/request';  // 引入 request.ts 中的 axios 实例
import Quill from 'quill'; // 引入 Quill 编辑器
import 'quill/dist/quill.snow.css'; // 引入 Quill 样式
import type { Note, GetNoteDetailResponse } from '@/types/api/getNotelist';

const route = useRoute();
const router = useRouter();
const noteId = route.params.id === 'new' ? 'new' : Number(route.params.id); // 确保类型正确
const isNewNote = noteId === 'new';
const folderId = Number(route.params.folder_id); // 从路由参数获取 folderId

// 检查传递的 title
const noteTitle = ref<string>(
  typeof route.params.title === 'string' ? route.params.title : '新建笔记0'
); // 获取传递过来的文件名称，如果没有则使用默认名称

// 调试：打印路由参数，检查是否正确传递了 title
console.log('Route Params:', route.params);

const note = ref<Note>({
  id: 0,
  user_id: 0,
  title: noteTitle.value,
  content: '',
  folder_id: folderId,
  tag: '',
  created_at: '',
  updated_at: '',
  deleted_at: null
});

// 初始化 Quill 编辑器
const quillEditor = ref<any>(null);

// 获取笔记详情
const fetchNote = async (note_id: string) => {
  try {
    const response = await request.get<GetNoteDetailResponse>('/ez-note/note/query', { params: { note_id } });
    if (response.code === 0) {
      const fetchedNote = response.data;
      note.value = { ...fetchedNote };
      if (quillEditor.value) {
        quillEditor.value.root.innerHTML = fetchedNote.content; // 填充 Quill 编辑器内容
      }
    } else {
      alert('未找到该笔记，返回上一页');
      router.push({ name: 'bjwjj' }); // 跳转到笔记列表页
    }
  } catch (error) {
    console.error('请求失败', error);
    alert('拉取笔记失败，请稍后重试');
  }
};

// 初始化新建笔记
const initNewNote = () => {
  note.value = {
    id: 0,
    user_id: 0,
    title: noteTitle.value,
    content: '',
    folder_id: folderId,
    tag: '默认',
    created_at: new Date().toISOString().slice(0, 10),
    updated_at: new Date().toISOString().slice(0, 10),
    deleted_at: null
  };
};

// 保存笔记
const saveNote = async () => {
  try {
    // 创建 FormData
    const formData = new FormData();
    formData.append('note_id', note.value.id || ''); // 如果是新建笔记，不发送 id
    formData.append('title', note.value.title);
    formData.append('content', quillEditor.value.root.innerHTML);
    formData.append('folder_id', note.value.folder_id);
    formData.append('tag', note.value.tag);

    // 设置请求的 URL
    const apiUrl = isNewNote ? '/ez-note/note/create' : '/ez-note/note/update/content';

    // 发送请求
    const response = await request.post(apiUrl, formData);

    // 根据响应处理
    if (response.code === 0) {
      alert(isNewNote ? '笔记创建成功' : '笔记更新成功');
      router.push({ name: 'bjwjj' }); // 跳转到笔记列表页面
    } else {
      alert(`保存失败：${response.msg}`);
    }
  } catch (error) {
    console.error('保存失败:', error);
    alert('保存失败，请稍后重试');
  }
};

// 取消编辑
const cancelEdit = () => {
  if (isNewNote) {
    router.push({ name: 'bjwjj' });
  } else {
    fetchNote(String(noteId));
  }
};

onMounted(() => {
  // 调试：检查 noteTitle 是否正确
  console.log('笔记标题:', noteTitle.value);

  if (isNewNote) {
    initNewNote();
  } else if (noteId) {
    fetchNote(String(noteId));
  }

  // 初始化 Quill 编辑器
  quillEditor.value = new Quill('#editor-container', {
    theme: 'snow', // 主题设置
    placeholder: '在这里输入内容...', // 默认提示文字
    modules: {
      toolbar: [
        [{ header: '1' }, { header: '2' }, { font: [] }],
        [{ list: 'ordered' }, { list: 'bullet' }],
        ['bold', 'italic', 'underline'],
        ['link'],
        ['blockquote', 'code-block'],
        ['image', 'video'],
      ],
    },
  });
});
</script>

<template>
  <div class="note-detail-container">
    <div class="note-form">
      <h2>{{ note.title || '新建笔记1' }}</h2>
      <!-- 使用 Quill 编辑器的容器 -->
      <div id="editor-container"></div>

      <label for="note-tag">标签</label>
      <input v-model="note.tag" id="note-tag" type="text" />

      <div class="actions">
        <button @click="saveNote">保存</button>
        <button @click="cancelEdit">取消</button>
      </div>
    </div>
  </div>
</template>



<style scoped>
.note-detail-container {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
}

.note-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.note-form label {
  font-weight: bold;
}

.note-form input,
.note-form textarea {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

#editor-container {
  height: 400px;
  /* 设置编辑器的高度 */
}

.actions {
  margin-top: 20px;
}

.actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}
</style>
