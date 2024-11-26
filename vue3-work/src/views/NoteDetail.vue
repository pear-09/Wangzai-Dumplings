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

const note = ref<Note>({
  id: 0,
  user_id: 0,
  title: noteTitle.value,
  content: '',
  folder_id: folderId,
  tags: ['no'],
  created_at: '',
  updated_at: '',
  deleted_at: null
});

// 初始化 Quill 编辑器
const quillEditor = ref<any>(null);
const isSummaryMode = ref(false); // 控制摘要模式
const selectedText = ref<string>(''); // 记录选中的文本
const showOptions = ref(false); // 控制“√”“×”的显示
const optionsPosition = ref({ x: 0, y: 0 }); // 选项按钮的位置
// 发送摘要接口请求（使用 FormData）
const sendSummary = async (text: string) => {
  try {
    // 创建 FormData 对象
    const formData = new FormData();
    formData.append('text', text);
    formData.append('AI_model', 1);
    // 发送 POST 请求
    const response = await request.post('/ez-note/AI/summary', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // 确保 Content-Type 设置为 multipart/form-data
      },
    });

    if (response.code === 0) {
      alert('摘要已发送');
    } else {
      console.error('摘要发送失败', response.msg);
    }
  } catch (error) {
    console.error('发送失败', error);
  }
};


// 进入摘要模式
const enableSummaryMode = () => {
  isSummaryMode.value = true;
  document.addEventListener('mouseup', handleTextSelection);
  sendAIMessage('生成摘要');
};

// 退出摘要模式
const disableSummaryMode = () => {
  isSummaryMode.value = false;
  selectedText.value = '';
  showOptions.value = false;
  document.removeEventListener('mouseup', handleTextSelection);
};

// 处理鼠标选中文本
const handleTextSelection = (event: MouseEvent) => {
  const selection = window.getSelection();
  const text = selection?.toString().trim();
  if (text) {
    selectedText.value = text;
    showOptions.value = true;
    optionsPosition.value = { x: event.pageX, y: event.pageY };
  } else {
    showOptions.value = false;
  }
};

// 点击“√”发送选中摘要
const confirmSelection = () => {
  if (selectedText.value) {
    sendSummary(selectedText.value);
  }
  showOptions.value = false;
};

// 点击“×”取消选中
const cancelSelection = () => {
  selectedText.value = '';
  showOptions.value = false;
};

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
    tags: [],
    created_at: new Date().toISOString().slice(0, 10),
    updated_at: new Date().toISOString().slice(0, 10),
    deleted_at: null
  };
};

const tagsInput = ref<string>(''); // 辅助字段
const showInput = ref(false); // 控制标签输入框的显示与隐藏

// 处理输入标签
const addTag = () => {
  if (tagsInput.value.trim()) {
    note.value.tags.push(tagsInput.value.trim());
    tagsInput.value = ''; // 清空输入框
    showInput.value = false; // 隐藏输入框，显示加号
  }
};

// 处理按回车键添加标签
const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    addTag();
  }
};

// 删除标签
const removeTag = (tag: string) => {
  note.value.tags = note.value.tags.filter(t => t !== tag);
};

// 更新 tags 字段
const updateTags = () => {
  // Tags 已通过输入框更新，因此可以通过上面的方法直接管理 tags
};

const saveTags = async () => {
  try {
    // 创建 FormData 对象
    const formData = new FormData();
    formData.append('note_id', note.value.id.toString()); // 传递 note_id
    note.value.tags.forEach(tag => formData.append('tag', tag)); // 逐个添加标签到 FormData

    // 调用更新标签的接口
    const response = await request.post('/ez-note/note/update/tag', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // 明确指定 multipart/form-data 类型
      },
    });

    if (response.code === 0) {
      console.log('标签更新成功');
    } else {
      console.error(`标签更新失败：${response.msg}`);
      alert(`标签更新失败：${response.msg}`);
    }
  } catch (error) {
    console.error('标签保存失败:', error);
    alert('标签保存失败，请稍后重试');
  }
};


const saveNote = async () => {
  try {
    // 创建 FormData
    const formData = new FormData();
    formData.append('note_id', note.value.id || ''); // 如果是新建笔记，不发送 id
    formData.append('title', note.value.title);
    formData.append('content', quillEditor.value.root.innerHTML);
    formData.append('folder_id', note.value.folder_id);

    // 设置请求的 URL
    const apiUrl = isNewNote ? '/ez-note/note/create' : '/ez-note/note/update/content';

    // 发送请求
    const response = await request.post(apiUrl, formData);

    // 根据响应处理
    if (response.code === 0) {
      alert(isNewNote ? '笔记创建成功' : '笔记更新成功');

      // 如果是新建笔记，从响应中更新 note 的 id
      if (isNewNote && response.data.id) {
        note.value.id = response.data.id;
      }

      // 调用标签更新方法
      await saveTags();

      router.push({ name: 'bjwjj' }); // 跳转到笔记列表页面
    } else {
      alert(`保存失败：${response.msg}`);
    }
  } catch (error) {
    console.error('保存失败:', error);
    alert('保存失败，请稍后重试');
  }
};


const cancelEdit = () => {
  // 判断是否为新建笔记
  if (isNewNote) {
    // 如果是新建笔记，直接跳转到笔记列表页面
    router.push({ name: 'bjwjj' }); // 'bjwjj' 是笔记列表页的路由名称
  } else {
    // 如果是编辑已有笔记，重新加载该笔记并跳转回笔记详情页
    fetchNote(String(noteId)); // 重新获取该笔记的数据
    router.push({ name: 'bjwjj'}); // 'noteDetail' 是编辑页的路由名称
  }
};

const showAIChat = ref(false); // 控制AI对话框的显示与隐藏
const aiMessages = ref<Array<{ sender: string, content: string }>>([]); // AI与用户的消息

// 切换AI对话框的显示/隐藏
const toggleAIChat = () => {
  showAIChat.value = !showAIChat.value;
};

// 发送AI消息
const sendAIMessage = (message: string) => {
  aiMessages.value.push({ sender: 'user', content: message }); // 用户的消息
  // 模拟AI的回复
  aiMessages.value.push({ sender: 'ai', content: `AI收到请求：${message}` });

  // 在这里你可以根据按钮内容发送请求到后端来获取AI的具体响应，模拟的AI回复可以替换为实际请求的响应
  // 例如: 
  // request.post('/ai/response', { query: message }).then(response => {
  //    aiMessages.value.push({ sender: 'ai', content: response.data });
  // });
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
  <div class="box">
    <div :class="['note-detail-container', { 'expanded': !showAIChat }]">
      <div class="note-form">
        <h2>{{ note.title || '新建笔记1' }}</h2>
        <!-- 使用 Quill 编辑器的容器 -->
        <div id="editor-container"></div>

        <label for="note-tag">标签</label>

        <!-- 显示标签卡片 -->
        <div class="tags-list">
          <div
            v-for="(tag, index) in note.tags"
            :key="index"
            class="tag-card"
          >
            {{ tag }}
            <button class="remove-btn" @click="removeTag(tag)">×</button>
          </div>
          <!-- 标签输入区域 -->
          <div class="tag-input-container">
            <button v-if="!showInput" class="add-btn" @click="showInput = true">+</button>
            <span v-if="showInput">
              <input
              v-model="tagsInput"
              id="note-tag"
              type="text"
              placeholder="输入标签"
              @keydown="handleKeydown"
            />
            <button class="add-btn" @click="showInput = false">X</button>
            </span>
          </div>
        </div>

        <div class="actions">
          <button @click="saveNote">保存</button>
          <button @click="cancelEdit">取消</button>
        </div>
      </div>
    </div>
    <!-- AI辅助对话框 -->
    <div v-if="showAIChat" class="ai-chat-container">
      <div class="ai-chat-header">
        <div class="title">
          笔记助手
        </div>
         <i class="iconfont icon-fangxiang-you" @click="toggleAIChat"></i>
      </div>
      <div class="ai-chat-body">
        <div v-for="(message, index) in aiMessages" :key="index" class="ai-chat-message">
          <div v-if="message.sender === 'user'" class="user-message">
            <span>{{ message.content }}</span>
          </div>
          <div v-else class="ai-message">
            <span>{{ message.content }}</span>
          </div>
        </div>
      </div>
      <div class="ai-chat-footer">
        <button @click="sendAIMessage('笔记美化')">笔记美化</button>
        <button @click="enableSummaryMode">生成摘要</button>
        <button @click="disableSummaryMode">退出摘要模式</button>
      </div>
      
    </div>

    <!-- AI辅助按钮 -->
    <button v-if="!showAIChat" class="ai-assist-btn" @click="toggleAIChat">AI辅助</button>
  </div>
   <!-- 摘要模式选项 -->
   <div
      v-if="showOptions"
      class="selection-options"
      :style="{ top: `${optionsPosition.y}px`, left: `${optionsPosition.x}px` }"
    >
      <button @click="confirmSelection">√</button>
      <button @click="cancelSelection">×</button>
    </div>
</template>

<style scoped>
.note-detail-container {
  width: 70%;
  padding: 20px;
  transition: width 0.3s ease;
}

.note-detail-container.expanded {
  width: 100%;
}

.ai-chat-container {
  width: 30%;
  height: 640px;
  background-color: #fff;
  margin-top: 100px;
  border-radius: 10px 0 0 10px;
  box-shadow: -4px 0 10px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
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

/* 标签输入部分 */
.tags-container {
  margin-bottom: 20px;
}

/* 标签卡片样式 */
.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-card {
  background-color: #f1f1f1;
  padding: 5px 10px;
  border-radius: 20px;
  display: flex;
  align-items: center;
}
input{
  border: none;
  outline: none;
  margin-right: 10px;
}
.remove-btn {
  margin-left: 8px;
  background: none;
  border: none;
  color: red;
  cursor: pointer;
}

.add-btn {
  width: 30px;
  height: 30px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 100%;
  /* padding: 6px 12px; */
  cursor: pointer;
}

.box {
  display: flex;
  position: relative; /* Add this to position the AI button in relation to the container */
}

.ai-assist-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 100px;
  height: 40px;
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.ai-chat-container {
  width: 30%;
  background-color: #fff;
  border-radius: 10px 0 0 10px;
  box-shadow: -4px 0 10px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.ai-chat-header {
  padding: 15px;
  background-color: #28a745;
  color: white;
  display: flex;
  justify-content: space-between;
}

.ai-chat-header .title{
  flex:1;
  text-align: center;
  font-weight: 600;
}


.ai-chat-header i{
  width: 10px;
}

.ai-chat-body {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background-color: #f9f9f9;
}

.ai-chat-footer {
  padding: 10px;
  background-color: #f1f1f1;
  display: flex;
  justify-content: space-around;
}

.ai-chat-footer button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
}

.ai-chat-message {
  margin-bottom: 10px;
}

.ai-chat-message .user-message {
  text-align: right;
}

.ai-chat-message .ai-message {
  text-align: left;
}

.ai-chat-message span {
  display: inline-block;
  background-color: #e1e1e1;
  padding: 8px;
  border-radius: 5px;
}
.note-container {
  position: relative;
}

.selection-options {
  position: absolute;
  display: flex;
  gap: 5px;
  background: white;
  border: 1px solid #ccc;
  padding: 5px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}
</style>
