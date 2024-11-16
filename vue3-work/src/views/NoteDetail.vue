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
// const noteId = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id;
const isNewNote = noteId === 'new'; 
const folderId = Number(route.params.folder_id); // 从路由参数获取 folderId
const note = ref<Note>({
  id: 0,
  user_id: 0,
  title: '',
  content: '',
  folder_id: folderId,
  tag: '',
  created_at: '',
  updated_at: '',
  deleted_at: null
});

const isEditing = ref(false);

// 初始化 Quill 编辑器
const quillEditor = ref<any>(null); 

const API_URL = import.meta.env.VITE_API_URL ;

// 获取笔记详情
const fetchNote = async (id: string) => {
  try {
    const response = await request.get<GetNoteDetailResponse>(`${API_URL}/ez-note/note/query`, { params: { id } });
    if (response.code === 0) {
      const fetchedNote = response.data;
      note.value = { ...fetchedNote };
      // 初始化 Quill 编辑器的内容
      if (quillEditor.value) {
        quillEditor.value.root.innerHTML = fetchedNote.content; // 将获取的笔记内容插入编辑器
      }
    }
  } catch (error) {
    console.error('请求失败', error);
  }
};

// 初始化新建笔记
const initNewNote = () => {
  note.value = {
    id: 0,
    user_id: 0,
    title: '',
    content: '',
    folder_id: folderId,
    tag: '默认',
    created_at: new Date().toISOString().slice(0, 10),
    updated_at: new Date().toISOString().slice(0, 10),
    deleted_at: null
  };
};

// 启动编辑模式
const startEditing = () => {
  isEditing.value = true;
  console.log(folderId)
};

// 保存笔记
const saveNote = async () => {
  try {
    // 准备数据
    const noteData = {
      title: note.value.title,
      content: quillEditor.value.root.innerHTML, // 从 Quill 编辑器获取内容
      folder_id: note.value.folder_id,
      tag: note.value.tag
    };

    // 创建 URL 编码格式的数据
    const urlEncodedData = new URLSearchParams();
    for (const [key, value] of Object.entries(noteData)) {
      urlEncodedData.append(key, value);
    }

    // 如果是新建笔记
    let response;
    if (isNewNote) {
      // 创建新笔记
      response = await request.post(`${API_URL}/ez-note/note/create`, urlEncodedData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
    } else {
      // 更新现有笔记
      response = await request.post(`${API_URL}/ez-note/note/update/content`, urlEncodedData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
    }

    // 处理响应
    if (response.code === 0) {
      // 成功后跳转到笔记列表页面
      router.push({ name: 'bjwjj' });
    } else {
      console.error('保存失败', response.msg);
    }
  } catch (error) {
    console.error('请求失败', error);
  }
};



// 取消编辑
const cancelEdit = () => {
  if (isNewNote) {
    router.push({ name: 'bjwjj' });
  } else {
    fetchNote(noteId);
  }
};

onMounted(() => {
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
    <h1 class="page-title">{{ isNewNote ? '新建笔记' : '编辑笔记' }}</h1>
    
    <div class="note-form">
      <label for="note-title">标题</label>
      <input v-model="note.title" id="note-title" type="text" :disabled="!isEditing" />

      <label for="note-content">内容</label>
      <!-- 使用 Quill 编辑器的容器 -->
      <div id="editor-container" :disabled="!isEditing"></div>

      <label for="note-tag">标签</label>
      <input v-model="note.tag" id="note-tag" type="text" :disabled="!isEditing" />

      <div class="actions">
        <button @click="saveNote" :disabled="!isEditing">保存</button>
        <button @click="cancelEdit">取消</button>
        <button v-if="!isEditing" @click="startEditing">编辑</button>
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
  height: 400px; /* 设置编辑器的高度 */
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
