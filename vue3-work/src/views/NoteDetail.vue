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
const currentMode = ref<string>(''); // 当前模式

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
const AI_model = ref(); 
const mode_name = ref<string>('');
const showOptions = ref(false); // 控制“√”“×”的显示
const optionsPosition = ref({ x: 0, y: 0 }); // 选项按钮的位置

// 弹窗显示状态
const showStudyPlanDialog = ref(false);
const days = ref(7); // 默认复习天数
const degree = ref('medium'); // 默认详细程度

//为每个模式单独定义一个接口调用函数，如调用名词解释、智能翻译等

const sendSummary = async (text: string, AI_model:number) => {
  // 发送生成摘要的请求
  await sendAIRequest('/ez-note/AI/summary', text, 'summary', AI_model);
};

const sendDefinition = async (text: string, AI_model:number) => {
  // 发送名词解释的请求
  await sendAIRequest('/ez-note/AI/explain', text, 'summary', AI_model);
};

const sendTranslation = async (text: string, AI_model:number) => {
  // 发送智能翻译的请求
  await sendAIRequest('/ez-note/AI/translate', text, 'translation',AI_model);
};

const sendKeywords = async (text: string, AI_model:number) => {
  // 发送提取关键词的请求
  await sendAIRequest('/ez-note/AI/keywords', text, 'keywords', AI_model);
};

const sendStudyPlan = async (text: string, AI_model:number) => {
  closeStudyPlanDialog();
  // 发送生成复习计划的请求
  await sendAIRequest('/ez-note/AI/plan', text, 'plan', AI_model);
};

const sendAIRequest = async (url: string, text: string, type: string, AI_model: number) => {
  // 创建一个新的 AI 消息，先设置为加载状态
  aiMessages.value.push({ sender: 'ai', content: '', loading: true });

  // 获取当前消息的索引
  const loadingMessageIndex = aiMessages.value.length - 1;

  try {
    const formData = new FormData();
    if(type === 'plan'){
      formData.append('text', text);
      formData.append('AI_model', AI_model);
      formData.append('days',days.value.toString());
      formData.append('degree',degree.value);
    }else{
      formData.append('text', text);
      formData.append('AI_model', AI_model);
    }
    // 发送请求
    const response = await request.post(url, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    if (response.code === 0) {
      // 请求成功，更新 AI 消息内容
      sendAIMessage(response, type);

      // 更新消息的内容，并移除加载状态
      aiMessages.value[loadingMessageIndex].content = response.data; // 将 AI 的实际回答填入消息
      aiMessages.value[loadingMessageIndex].loading = false; // 取消加载状态
    } else {
      console.error('请求失败', response.msg);
      // 更新失败消息内容
      aiMessages.value[loadingMessageIndex].content = '请求失败，请稍后重试';
      aiMessages.value[loadingMessageIndex].loading = false;
    }
  } catch (error) {
    console.error('请求发送失败', error);
    // 请求发送失败时更新消息内容
    aiMessages.value[loadingMessageIndex].content = '请求发送失败，请检查网络';
    aiMessages.value[loadingMessageIndex].loading = false;
  }
};

//模式确认
const confirmMode = (mode: string,name: string) => {
  currentMode.value = mode;
  // 发送模式确认消息到 AI 聊天窗口
  aiMessages.value.push({ sender: 'user', content: name });

  // AI 立即回复
  switch (mode) {
    case 'summary':
      aiMessages.value.push({ sender: 'ai', content: '您已切换到摘要模式，请选中文本生成摘要。', loading: false});
      break;
    case 'translation':
      aiMessages.value.push({ sender: 'ai', content: '您已切换到翻译模式，请选中文本进行翻译。', loading: false });
      break;
    case 'definition':
      aiMessages.value.push({ sender: 'ai', content: '您已切换到名词解释模式，请选中文本查看解释。', loading: false });
      break;
    case 'keywords':
      aiMessages.value.push({ sender: 'ai', content: '您已切换到提取关键词模式，请选中文本提取关键词。', loading: false });
      break;
    case 'studyPlan':
      aiMessages.value.push({ sender: 'ai', content: '您已切换到生成复习计划模式，请选中文本生成计划。', loading: false });
      break;
    default:
      aiMessages.value.push({ sender: 'ai', content: '未知模式，请重新选择。', loading: false });
  }
};

//创建一个函数，用于根据点击的按钮切换模式：
const setMode = (mode: string,name: string) => {
  currentMode.value = mode;
  document.addEventListener('mouseup', handleTextSelection);
  confirmMode(mode,name);
  if(mode === 'studyPlan'){
    openStudyPlanDialog();
  }
}
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
//在确认选中文本时，根据 currentMode 调用不同的接口：
const confirmSelection = () => {
  if (!selectedText.value) return;
  switch (currentMode.value) {
    case 'summary':
      sendSummary(selectedText.value, AI_model.value);
      break;
    case 'definition':
      sendDefinition(selectedText.value, AI_model.value);
      break;
    case 'translation':
      sendTranslation(selectedText.value, AI_model.value);
      break;
    case 'keywords':
      sendKeywords(selectedText.value, AI_model.value);
      break;
    default:
      console.error('未知模式');
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
    tags: ['默认标签'],
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
const loading = ref(false);  // 控制加载状态
const aiMessages = ref<Array<{ sender: string, content: string, loading:boolean}>>([]); // AI与用户的消息
const showPage1 = ref(true);
const isSuccess = ref(false);
// 切换AI对话框的显示/隐藏
// 退出摘要模式
const toggleAIChat = (mode:number) => {
  showAIChat.value = !showAIChat.value;
  isSummaryMode.value = false;
  selectedText.value = '';
  showOptions.value = false;
  AI_model.value = mode;
  if(mode===1){
    mode_name.value = 'KIMI';
  }else
    mode_name.value = 'Chat GPT';
  document.removeEventListener('mouseup', handleTextSelection);
};

const toggleshowPage = () => {
  showPage1.value = !showPage1.value;
};

// 发送AI消息
const sendAIMessage = (response: any, type: string) => {
 switch (type) {
    case 'translation':
      aiMessages.value.push({ sender: 'ai', content: response.translation, loading:false });
      break;
    case 'summary':
      aiMessages.value.push({ sender: 'ai', content: response.summary, loading:false  });
      break;
    case 'keywords':
      aiMessages.value.push({ sender: 'ai', content: response.keywords, loading:false  });
      break;
    case 'explanation':
      aiMessages.value.push({ sender: 'ai', content: response.summary, loading:false  });
      break;
    case 'plan':
    aiMessages.value.push({ sender: 'ai', content: response.plan, loading:false  });
    break;
    default:
      console.warn('未知类型:', type);
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

// 打开生成复习计划的弹窗
const openStudyPlanDialog = () => {
  showStudyPlanDialog.value = true;
};

// 关闭弹窗
const closeStudyPlanDialog = () => {
  showStudyPlanDialog.value = false;
};

</script>

<template>
  <div class="box">
    <div :class="['note-detail-container', { 'expanded': !showAIChat }]">
      <div class="note-form">
        <h2>{{ note.title || '新建笔记1' }}</h2>
        <!-- 使用 Quill 编辑器的容器 -->
        <div id="editor-container"></div>

        <label for="note-tag">标签 :</label>

        <!-- 显示标签卡片 -->
        <div class="tags-list">
          <div
            v-for="(tag, index) in note.tags"
            :key="index"
            class="tag-card"
          >
            <i class="iconfont icon-hashjinghao"></i>
            {{ tag }}
            <button class="remove-btn" @click="removeTag(tag)">
              <i class="iconfont icon-cuo"></i>
            </button>
          </div>
          <!-- 标签输入区域 -->
          <div class="tag-input-container">
            <i v-if="!showInput" @click="showInput = true" class="iconfont icon-tianjia-"></i>
            <span v-if="showInput">
              <input
              class="addtag"
              v-model="tagsInput"
              id="note-tag"
              type="text"
              placeholder="输入标签 ..."
              @keydown="handleKeydown"
            />
            <button class="add-btn" @click="addTag">
              <i class="iconfont icon-huiche" style="font-size: 12px;"></i>
            </button>
            <button class="add-btn" @click="showInput = false">
              <i class="iconfont icon-cuo" style="font-size: 14px; font-weight: 600;"></i>
            </button>
            </span>
          </div>
        </div>

        <div class="actions">
          <button class="btn1" @click="saveNote">保存</button>
          <button class="btn2" @click="cancelEdit">取消</button>
        </div>
      </div>
    </div>
    <!-- AI辅助对话框 -->
    <div v-if="showAIChat" class="ai-chat-container">
      <div class="ai-chat-header">
        <div class="title">
          {{mode_name}}
        </div>
        <!-- 退出ai模式 -->
        <i @click="toggleAIChat(AI_model)" class="iconfont icon-fangxiang-you"></i>
      </div>
      <div class="ai-chat-body">
        <div v-for="(message, index) in aiMessages" :key="index" class="ai-chat-message">
           <!-- 用户消息 -->
          <div v-if="message.sender === 'user'" class="user-message">
            <span>{{ message.content }}</span>
          </div>
            <!-- AI消息 -->
            <div v-else class="ai-message">
            <!-- 只有当有内容或正在加载时才显示头像 -->
            <div v-if="message.loading || message.content" class="ai-avatar">
              <i class="iconfont icon-gpt1"></i>
            </div>

            <!-- 如果该消息正在加载，显示加载动画 -->
            <span v-if="message.loading">
              <div class="loading-spinner">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
              </div>
            </span>

            <!-- 如果消息已经加载完成，则显示实际内容 -->
            <span v-else v-if="message.content">
              <div class="content">{{ message.content }}</div>
            </span>
          </div>

        </div>
      </div>
      <!-- <div v-if="isSuccess" class="tools">
        <button>替换</button>
        <button>重新</button>
        <button>编辑</button>
      </div> -->
      <div class="ai-chat-footer">
        <div v-if="showPage1" class="page1">
          <button @click="setMode('summary','生成摘要')">生成摘要</button>
          <button @click="setMode('definition','名词解释')">名词解释</button>
          <button @click="setMode('translation','智能翻译')">智能翻译</button>
        </div>
        <div v-else class="page2">
          <button @click="setMode('keywords','提取关键词')">提取关键词</button>
          <button @click="setMode('studyPlan','生成复习计划')">生成复习计划</button>
        </div>
        <button class="next" @click="toggleshowPage">
          <i class="iconfont icon-fangxiang-you"></i>
        </button>
      </div>
    </div>

    <!-- AI辅助按钮 -->
    <div v-if="!showAIChat" class="btn-box">
      <button class="ai-assist-btn" @click="toggleAIChat(1)">KIMI</button>
      <button class="ai-assist-btn"  @click="toggleAIChat(0)">GPT</button>
    </div>
    
  </div>

<!-- 模式选项 -->
<div
  v-if="showOptions"
  class="selection-options"
  :style="{ top: `${optionsPosition.y}px`, left: `${optionsPosition.x}px` }"
>
  <button @click="confirmSelection" class="option-btn confirm-btn">√</button>
  <button @click="cancelSelection" class="option-btn cancel-btn">×</button>
</div>

<!-- 弹窗：输入天数，选择计划详细程度 -->
<div v-if="showStudyPlanDialog" class="modal">
  <div class="modal-content">
    <h3 class="modal-title">生成复习计划</h3>
    <label for="days">复习天数：</label>
    <input type="number" v-model="days" id="days" min="1" max="14" required class="input-field"/>

    <label for="degree">计划详细程度：</label>
    <select v-model="degree" id="degree" class="input-field">
      <option value="low">简单</option>
      <option value="medium" selected>中等</option>
      <option value="high">详细</option>
    </select>

    <div class="modal-buttons">
      <button @click="sendStudyPlan(note.content, AI_model), showStudyPlanDialog = false;" class="btn confirm-btn">生成计划</button>
      <button @click="closeStudyPlanDialog" class="btn cancel-btn">取消</button>
    </div>
  </div>
</div>

</template>

<style scoped>
.note-detail-container {
  width: 70%;
  padding: 20px;
  padding-top: 0px;
  margin-top: 0px;
  transition: width 0.3s ease;
}

.note-detail-container.expanded {
  width: 100%;
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

h2{
  margin-bottom: 5px;
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
  height: 360px;
  /* 设置编辑器的高度 */
}

.actions {
  margin-top: 5px;
}

.actions button {
  width: 80px;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
  color: #fff;
}

.actions .btn1{
  background-color:#759a8b;
}

.actions .btn2{
  background-color: #c7184a;
}

.actions .btn1:hover{
  background-color:#67897b;
}

.actions .btn2:hover{
  background-color:#892923;
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
  padding: 8px;
  /* padding-left: 15px; */
  border-radius: 10px;
  display: flex;
  align-items: center;
}
 
.tag-card .icon-hashjinghao{
  /* font-size: 10px; */
  font-weight: 600;
  transform: translateY(1px);
  margin-right: 2px;
  color: #28a745;
}

.tag-card .remove-btn .icon-cuo{
  /* margin-left: 5px; */
  font-weight: 700;
  font-size: 20px;
  color: rgb(202, 38, 38);
  transition: all .5s ease;
}

.tag-card .remove-btn .icon-cuo:hover{
  color: red;

}

.icon-tianjia-{
  font-size: 38px;
  color: #28a745;
}
.icon-tianjia-:hover{
  color: #228037;
  font-size: 39px;
}

.tag-input-container .addtag{
  border: none;
  border-bottom: solid 1px #228037;
  border-radius: 0;
  background: none;
  outline: none;
  margin-right: 10px;
  transform: translateY(2px);
  cursor: pointer;
}
.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  transform: translateY(-4px);
}

.add-btn {
  width: 30px;
  height: 30px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 100%;
  /* padding: 6px 12px; */
  margin-right: 5px;
  cursor: pointer;
  transform: translateY(2px);
}

.box {
  display: flex;
  position: relative; /* Add this to position the AI button in relation to the container */
}

.btn-box{
  width: 210px;
  height: 60px;
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  justify-content: space-between;
}

.btn-box .ai-assist-btn{
  width: 100px;
  height: 40px;
  background-color: #759a8b;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-box .ai-assist-btn:hover{
  background-color: #67897b;
}

.ai-chat-container {
  width: 30%;
  height: 700px;
  background-color: #fff;
  margin-top: 0px;
  border-radius: 10px 0 0 10px;
  box-shadow: -4px 0 10px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.ai-chat-header {
  padding: 15px;
  background-color: #759a8b;
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
  width: 100%;
  padding: 10px;
  background-color: #f1f1f1;
  display: flex;
  justify-content: space-between;
}

.ai-chat-footer .page1{
  width: 90%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.ai-chat-footer .page2 {
  width: 90%;
  display: flex;
  align-items: center;
}

.ai-chat-footer .page2 button{
  width: 120px;
  margin-left: 20px;
  margin-right: 20px;
}

.ai-chat-footer .next{
  width: 10%;
  height: 40px;
  margin-right: 5px;
  background-color: transparent;
}

.ai-chat-footer button {
  width: 100px;
  height: 40px;
  background-color: #88b791;
  color: white;
  border: none;
  padding: 5px;
  cursor: pointer;
  border-radius: 20px;
}

.ai-chat-footer .next i{
  font-size: 20px;
  color: #28a745;
}

.ai-chat-message {
  margin-bottom: 10px;
}

.ai-chat-message .user-message {
  text-align: right;
  margin-top: 5px;
  margin-bottom: 5px;
}

/* 用户消息气泡 */
.ai-chat-message .user-message span {
  background-color: #28a745; /* 绿色背景 */
  color: white; /* 文字颜色 */
  padding: 10px;
  border-radius: 5px;
}

.ai-chat-message .ai-message {
  text-align: left;
  display: flex;
}

.ai-avatar {
  /* width: 35px;
  height: 35px;
  display: flex;
  justify-content: center; */
  align-items: center;
  /* padding: 5px;
  border-radius: 50%; 头像圆形
  margin-right: 5px; 头像与消息之间的间距 */
}

.ai-avatar i {
  width: 35px;
  height: 35px;
  margin: auto;
  font-size: 35px;
  margin-right: 5px;
}

.ai-message{
  margin-top: 5px;
  margin-bottom: 5px;
}

.ai-message span {
  background-color: #e1e1e1;
  padding: 8px;
  border-radius: 5px;
}

.ai-message span .content {
  transform: translateX(5px);
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

/* 加载动画样式 */
.loading-spinner {
  display: flex;
  align-items: center;
  gap: 5px;  /* 圆点之间的间距 */
  transform: translateY(5px);
}

/* 小圆点样式 */
.loading-spinner .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #28a745;
  animation: bounce 1.5s infinite ease-in-out;
}

/* 给每个圆点设置不同的动画延迟，实现跳动效果 */
.loading-spinner .dot:nth-child(1) {
  animation-delay: 0s;
}
.loading-spinner .dot:nth-child(2) {
  animation-delay: 0.2s;
}
.loading-spinner .dot:nth-child(3) {
  animation-delay: 0.4s;
}

/* 跳动动画 */
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);  /* 上下跳动的距离 */
  }
}

/* 弹窗背景 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* 半透明背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 确保弹窗位于最上层 */
  padding: 20px;
}

/* 弹窗内容 */
.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  width: 350px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 软阴影 */
  /* text-align: center; */
}

/* 弹窗标题 */
.modal-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

/* 输入框和下拉框 */
.input-field {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

/* 按钮通用样式 */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn:hover {
  transform: scale(1.05); /* 鼠标悬停时放大按钮 */
}

/* 确认按钮样式 */
.confirm-btn {
  background-color: #4CAF50;
  color: white;
}

.confirm-btn:hover {
  background-color: #45a049;
}

/* 取消按钮样式 */
.cancel-btn {
  background-color: #f44336; 
  color: white;
}

.cancel-btn:hover {
  background-color: #e53935;
}

/* 按钮容器 */
.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

/* 模式选项按钮 */
.selection-options {
  position: absolute;
  background-color: #fff;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 软阴影 */
}

.option-btn {
  font-size: 20px;
  padding: 10px;
  border: none;
  background-color: transparent;
  cursor: pointer;
  transition: color 0.2s ease;
}

.option-btn:hover {
  color: #007bff;
}

.confirm-btn {
  font-weight: bold;
}


</style>
